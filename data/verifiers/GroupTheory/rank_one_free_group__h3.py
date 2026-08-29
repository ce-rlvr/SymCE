import sympy
from sympy.combinatorics import free_group

# Top-level setup
try:
    F1, _ = free_group("x")
    F2, _ = free_group("x y")
    F3, _ = free_group("x y z")
except Exception:
    pass

def conditions(witness):
    try:
        # The witness can be a tuple (F, S) or just F
        if isinstance(witness, tuple) and len(witness) == 2:
            F, S = witness
        else:
            F = witness
            S = F.generators
    except Exception:
        return [False, False, False]

    # H1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # H2: S is a free generating set of F
    try:
        h2 = False
        if h1:
            # Handle the case where S is a single element instead of a collection
            if hasattr(S, 'group') and S.group == F:
                S_list = [S]
            else:
                S_list = list(S)
                
            # For simplicity and safety, we verify that S is exactly the standard free generating set.
            # (Any valid counterexample can simply use the standard generators).
            if set(S_list) == set(F.generators):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: F is not isomorphic to Z
    # A free group is isomorphic to Z iff its rank is 1
    try:
        if h1:
            neg_q = len(F.generators) != 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: S is a free generating set of F",
    "¬Q: F is not isomorphic to the additive group of integers Z"
]

N_HYP = 2
NEG_Q_INDEX = 2