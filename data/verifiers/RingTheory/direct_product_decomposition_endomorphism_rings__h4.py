import math
import sympy

# Top-level setup: named object bindings that the witness expression may reference.
# We represent Z-modules as lists of invariant factors (integers).
# 0 represents Z, n represents Z/nZ.
Z = [0]
Z2 = [2]
Z3 = [3]
Z4 = [4]
Z5 = [5]
Z6 = [6]
Z7 = [7]
Z8 = [8]
Z9 = [9]
Z10 = [10]
Z12 = [12]

def hom_Z_size(a, b):
    a = abs(int(a))
    b = abs(int(b))
    if a == 1 or b == 1:
        return 1
    if a == 0 and b == 0:
        return 0 # 0 means infinite size (Z)
    if a == 0 and b > 0:
        return b
    if a > 0 and b == 0:
        return 1
    if a > 0 and b > 0:
        return math.gcd(a, b)

def is_hom_zero(M1, M2):
    for a in M1:
        for b in M2:
            if hom_Z_size(a, b) != 1:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'Z')
            M1 = witness.get('M1', [])
            M2 = witness.get('M2', [])
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            R = 'Z'
            M1, M2 = witness
        else:
            return [False, False, False, False]
            
        if isinstance(M1, (int, sympy.Integer)): M1 = [int(M1)]
        if isinstance(M2, (int, sympy.Integer)): M2 = [int(M2)]
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring
    try:
        valid_R = ['Z', 'ZZ', 'Integers', sympy.S.Integers]
        h1 = (R in valid_R)
    except Exception:
        h1 = False

    # H2: M1 and M2 are R-modules
    try:
        def is_Z_module(M):
            if not isinstance(M, list): return False
            for x in M:
                if not isinstance(x, (int, sympy.Integer)):
                    return False
            return True
        h2 = is_Z_module(M1) and is_Z_module(M2)
    except Exception:
        h2 = False

    # H3: Hom_R(M1, M2) == {0}
    try:
        h3 = is_hom_zero(M1, M2) if h2 else False
    except Exception:
        h3 = False

    # neg_Q: End_R(M1 \oplus M2) is not isomorphic to End_R(M1) x End_R(M2)
    # For finitely generated Z-modules with Hom(M1, M2) = 0, 
    # the endomorphism rings are isomorphic iff Hom(M2, M1) = 0.
    try:
        neg_q = not is_hom_zero(M2, M1) if h2 else False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M1 and M2 are R-modules",
    "H_3: Hom_R(M1, M2) = {0}",
    "¬Q: End_R(M1 ⊕ M2) is not isomorphic to End_R(M1) × End_R(M2)"
]

N_HYP = 3
NEG_Q_INDEX = 3