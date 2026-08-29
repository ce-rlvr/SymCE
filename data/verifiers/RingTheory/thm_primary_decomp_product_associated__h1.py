import sympy
from sympy import *
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: I is a proper ideal of R
    h1 = False
    try:
        for attr in ['is_proper_ideal', 'is_proper']:
            if hasattr(witness, attr):
                val = getattr(witness, attr)
                h1 = bool(val() if callable(val) else val)
                break
            elif isinstance(witness, dict) and attr in witness:
                val = witness[attr]
                h1 = bool(val() if callable(val) else val)
                break
    except Exception:
        pass

    # H2: P_1, ..., P_k are the associated prime ideals of the minimal primary decomposition of I
    h2 = False
    try:
        for attr in ['is_minimal_primary_decomposition', 'has_minimal_primary_decomposition']:
            if hasattr(witness, attr):
                val = getattr(witness, attr)
                h2 = bool(val() if callable(val) else val)
                break
            elif isinstance(witness, dict) and attr in witness:
                val = witness[attr]
                h2 = bool(val() if callable(val) else val)
                break
    except Exception:
        pass

    # neg_Q: For all m > 0, (P_1 P_2 ... P_k)^m is NOT contained in I
    neg_q = False
    try:
        math_success = False
        # Attempt to compute containment mathematically if the witness provides I and P_list
        if hasattr(witness, 'I') and hasattr(witness, 'P_list'):
            try:
                I = witness.I
                P_list = witness.P_list
                if P_list:
                    P_prod = P_list[0]
                    for P in P_list[1:]:
                        P_prod = P_prod * P
                    
                    contained_any = False
                    for m in range(1, 30):
                        Pm = P_prod ** m
                        if hasattr(Pm, 'issubset'):
                            contained = Pm.issubset(I)
                        elif hasattr(I, 'contains'):
                            contained = I.contains(Pm)
                        else:
                            contained = (Pm in I)
                        
                        if contained:
                            contained_any = True
                            break
                    neg_q = not contained_any
                    math_success = True
            except Exception:
                pass
        
        # Fallback to property-based checking if math evaluation fails or is not applicable
        if not math_success:
            can_check = False
            contained_any = False
            for m in range(1, 30):
                contained = None
                for attr in ['product_power_contained', 'is_product_power_contained']:
                    if hasattr(witness, attr):
                        val = getattr(witness, attr)
                        contained = val(m) if callable(val) else val[m]
                        can_check = True
                        break
                    elif isinstance(witness, dict) and attr in witness:
                        val = witness[attr]
                        contained = val(m) if callable(val) else val[m]
                        can_check = True
                        break
                
                if contained:
                    contained_any = True
                    break
            
            if can_check:
                neg_q = not contained_any
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: P_1, P_2, ..., P_k are the associated prime ideals of the minimal primary decomposition of I",
    "¬Q: For all positive integers m, the product (P_1 P_2 ... P_k)^m is not contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2