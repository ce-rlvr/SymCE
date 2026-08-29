import sympy
from sympy import Symbol
from sympy.abc import x, y, z

# Top-level setup for standard objects
ZZ = sympy.ZZ
QQ = sympy.QQ

def get_Z_multiple(obj):
    """
    Helper to interpret the witness as a multiple of Z.
    Returns m for m*Z.
    """
    if isinstance(obj, (int, sympy.Integer)):
        return int(obj)
    if obj is sympy.ZZ:
        return 1
    if isinstance(obj, str):
        s = obj.strip().upper()
        if s.endswith('Z') or s.endswith('ZZ'):
            s = s.rstrip('Z')
            if s == '': return 1
            if s == '0': return 0
            try:
                return int(s)
            except ValueError:
                pass
    if isinstance(obj, tuple) and len(obj) == 2:
        if obj[1] in ('Z', 'ZZ', sympy.ZZ):
            if isinstance(obj[0], (int, sympy.Integer)):
                return int(obj[0])
    return None

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The standard counterexample involves non-unital rings, typically m*Z.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        
        R_obj, I_obj, x_obj = witness
        
        m = get_Z_multiple(R_obj)
        n = get_Z_multiple(I_obj)
        
        if m is None or n is None:
            return [False, False, False]
            
        # H_1: I is an ideal of R
        # In the context of Z-multiples, nZ is an ideal of mZ iff n is a multiple of m
        if m == 0:
            h1_ok = (n == 0)
        else:
            h1_ok = (n % m == 0)
            
        # H_2: x is an indeterminate
        h2_ok = isinstance(x_obj, sympy.Symbol) or (isinstance(x_obj, str) and x_obj.isalpha())
        
        # neg_Q: The polynomial ring over R mod I is NOT isomorphic to the quotient ring R poly mod I R poly
        # For R = mZ, I = nZ:
        # The base ring of the first is mZ / nZ, which has size |n/m| (if m != 0).
        # The base ring of the second is mZ / nmZ, which has size |nm/m| = |n|.
        # They are isomorphic if and only if their base rings have the same size, i.e., |n/m| == |n|.
        if m == 0 or n == 0:
            neg_q_ok = False
        else:
            neg_q_ok = (abs(n // m) != abs(n))
            
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: x is an indeterminate",
    "¬Q: The polynomial rings are not isomorphic"
]

N_HYP = 2
NEG_Q_INDEX = 2