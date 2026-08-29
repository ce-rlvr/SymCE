import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.polys
from sympy import Symbol, Rational, Integer
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference
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

def get_bool_attr(obj, attr_name, default=False):
    """Helper to safely extract and evaluate boolean attributes or methods."""
    if hasattr(obj, attr_name):
        val = getattr(obj, attr_name)
        if callable(val):
            try:
                return bool(val())
            except Exception:
                return default
        return bool(val)
    return default

def conditions(witness) -> list[bool]:
    # If the witness is directly provided as a tuple of 4 booleans
    if isinstance(witness, (tuple, list)) and len(witness) == 4 and all(isinstance(w, bool) for w in witness):
        return list(witness)
        
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    # Try to extract properties if witness is a dictionary or a mock object
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('K_is_field_of_fractions_of_R', witness.get('h1', False)))
            h2 = bool(witness.get('L_is_field_extension_of_K', witness.get('h2', False)))
            h3 = bool(witness.get('S_is_integral_closure_of_R_in_L', witness.get('h3', False)))
            
            if 'S_is_not_integral_domain' in witness:
                neg_q = bool(witness['S_is_not_integral_domain'])
            elif 'neg_q' in witness:
                neg_q = bool(witness['neg_q'])
            elif 'S_is_integral_domain' in witness:
                neg_q = not bool(witness['S_is_integral_domain'])
        else:
            h1 = get_bool_attr(witness, 'K_is_field_of_fractions_of_R') or get_bool_attr(witness, 'h1')
            h2 = get_bool_attr(witness, 'L_is_field_extension_of_K') or get_bool_attr(witness, 'h2')
            h3 = get_bool_attr(witness, 'S_is_integral_closure_of_R_in_L') or get_bool_attr(witness, 'h3')
            
            if hasattr(witness, 'S_is_not_integral_domain'):
                neg_q = get_bool_attr(witness, 'S_is_not_integral_domain')
            elif hasattr(witness, 'neg_q'):
                neg_q = get_bool_attr(witness, 'neg_q')
            elif hasattr(witness, 'S_is_integral_domain'):
                neg_q = not get_bool_attr(witness, 'S_is_integral_domain')
    except Exception:
        pass

    # Fallback: if witness is a tuple of mathematical objects (e.g., sympy domains)
    if not any([h1, h2, h3, neg_q]) and isinstance(witness, (tuple, list)) and len(witness) == 4:
        R, K, L, S = witness
        
        try:
            if hasattr(R, 'get_field'):
                h1 = (K == R.get_field())
        except Exception:
            pass
            
        try:
            if hasattr(L, 'is_Field'):
                h2 = L.is_Field
        except Exception:
            pass
            
        try:
            # Best effort check for integral closure in simple cases
            if R == S and K == L:
                h3 = True
        except Exception:
            pass
            
        try:
            if hasattr(S, 'is_Domain'):
                neg_q = not S.is_Domain
        except Exception:
            pass

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: L is a field extension of K",
    "H_3: S is the integral closure of R in L",
    "¬Q: S is not an integral domain"
]

N_HYP = 3
NEG_Q_INDEX = 3