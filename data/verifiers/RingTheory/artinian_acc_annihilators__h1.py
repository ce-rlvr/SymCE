import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.polys
from sympy.abc import *
import math
import itertools
import functools
import z3

# Top-level setup
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        # Rings that are known to satisfy ACC on annihilators
        if hasattr(witness, 'is_Noetherian') and witness.is_Noetherian:
            return [False]
        if hasattr(witness, 'is_integral_domain') and witness.is_integral_domain:
            return [False]
        if hasattr(witness, 'is_Field') and witness.is_Field:
            return [False]
        if hasattr(witness, 'is_finite') and witness.is_finite:
            return [False]
            
        # Check for custom properties on the witness object
        if hasattr(witness, 'satisfies_acc_on_annihilators'):
            val = witness.satisfies_acc_on_annihilators
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'has_acc_on_annihilators'):
            val = witness.has_acc_on_annihilators
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_acc_on_annihilators'):
            val = witness.is_acc_on_annihilators
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'acc_on_annihilators'):
            val = witness.acc_on_annihilators
            neg_q = not bool(val() if callable(val) else val)
        elif isinstance(witness, str):
            s = witness.lower()
            # A ring failing ACC on annihilators must be infinite and not an integral domain.
            # Common examples: infinite direct products, or infinite polynomial rings modulo ideals.
            if ("infinite" in s or "infty" in s or "..." in s):
                if "prod" in s or "sum" in s or "oplus" in s or "times" in s or "x" in s:
                    neg_q = True
                elif "/" in s or "mod" in s or "quotient" in s:
                    neg_q = True
    except Exception:
        pass
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: The ring R does not satisfy the ascending chain condition on both right annihilators and left annihilators"
]
N_HYP = 0
NEG_Q_INDEX = 0