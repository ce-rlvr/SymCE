import sympy
from sympy import S, Set, Interval, FiniteSet, Union, Intersection

# Top-level setup for witness expressions
Reals = S.Reals
EmptySet = S.EmptySet

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If K is a compact subset of a metric space X, and F is a subset of K, then F is compact."
    (The missing hypothesis is that F must be closed).
    
    The witness can be a tuple (K, F) of SymPy sets, or just F (in which case K = F.closure).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, F = witness
        else:
            F = witness
            K = F.closure
    except Exception:
        return [False, False, False, False]

    def is_compact(S_set):
        if S_set == S.EmptySet:
            return True
        if not isinstance(S_set, Set):
            return False
        if S_set.is_subset(S.Reals) != True:
            return False
        try:
            inf_val = S_set.inf
            sup_val = S_set.sup
            if inf_val is None or sup_val is None:
                return False
            # In R, compact implies bounded
            if not (inf_val.is_finite and sup_val.is_finite):
                return False
            # In R, compact implies closed (contains its boundary)
            if S_set.boundary.is_subset(S_set) != True:
                return False
            return True
        except Exception:
            return False

    # H_1: (X, d) is a metric space. 
    # We verify this by checking that K and F are subsets of the real line R, 
    # which is a standard metric space.
    try:
        h1 = (isinstance(K, Set) and isinstance(F, Set) and 
              K.is_subset(S.Reals) == True and F.is_subset(S.Reals) == True)
    except Exception:
        h1 = False

    # H_2: K is a compact subset of X
    try:
        h2 = is_compact(K)
    except Exception:
        h2 = False

    # H_3: F \subseteq K
    try:
        h3 = (F.is_subset(K) == True)
    except Exception:
        h3 = False

    # ¬Q: F is NOT compact
    try:
        neg_q = not is_compact(F)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: K is a compact subset of X",
    "H_3: F is a subset of K",
    "¬Q: F is not compact"
]

N_HYP = 3
NEG_Q_INDEX = 3