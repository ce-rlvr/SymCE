import sympy
from sympy.combinatorics import PermutationGroup, AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

Q_add = "Q_add"
R_add = "R_add"
C_add = "C_add"
Z_add = "Z_add"
Q_star = "Q_star"
R_star = "R_star"
C_star = "C_star"

def is_group(X):
    if type(X).__name__ in ['PermutationGroup', 'FpGroup', 'FreeGroup', 'AlternatingGroup', 'SymmetricGroup', 'CyclicGroup', 'DihedralGroup']:
        return True
    if hasattr(X, 'is_group') and X.is_group:
        return True
    if X in [sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, sympy.S.Integers]:
        return True
    if isinstance(X, str) and X in ["Q_add", "R_add", "C_add", "Z_add", "Q_star", "R_star", "C_star"]:
        return True
    if hasattr(X, 'elements') and hasattr(X, 'identity'):
        return True
    return False

def is_finitely_generated(X):
    if type(X).__name__ in ['PermutationGroup', 'FpGroup', 'AlternatingGroup', 'SymmetricGroup', 'CyclicGroup', 'DihedralGroup']:
        return True
    if type(X).__name__ == 'FreeGroup':
        try:
            return len(X.generators) < float('inf')
        except Exception:
            return True
    if X == sympy.S.Integers:
        return True
    if X in [sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
        return False
    if isinstance(X, str):
        if X == "Z_add":
            return True
        if X in ["Q_add", "R_add", "C_add", "Q_star", "R_star", "C_star"]:
            return False
    try:
        if hasattr(X, 'order') and callable(X.order) and X.order() < float('inf'):
            return True
        if hasattr(X, 'order') and not callable(X.order) and X.order < float('inf'):
            return True
    except Exception:
        pass
    try:
        if hasattr(X, 'is_finite') and X.is_finite:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1_ok = bool(is_group(G) and is_group(H))
    except Exception:
        h1_ok = False

    # H_2: G is a finitely generated group
    try:
        h2_ok = bool(is_group(G) and is_finitely_generated(G))
    except Exception:
        h2_ok = False

    # ¬Q: H is not a finitely generated group
    try:
        neg_q_ok = bool(is_group(H) and not is_finitely_generated(H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a finitely generated group",
    "¬Q: H is not a finitely generated group"
]

N_HYP = 2
NEG_Q_INDEX = 2