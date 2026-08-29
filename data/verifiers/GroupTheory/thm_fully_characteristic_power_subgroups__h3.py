import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        F, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False
        
    # H_2: n is a positive integer
    try:
        n_val = int(n)
        h2 = (n_val == n) and (n_val > 0)
    except Exception:
        h2 = False
        
    # ¬Q: F^n is not a fully characteristic subgroup of F
    # In the context of this false conjecture, F^n denotes the SET of n-th powers.
    # The set of n-th powers is a subgroup if and only if n == 1 or F is abelian (rank <= 1).
    # If it is not a subgroup, it cannot be a fully characteristic subgroup.
    try:
        if h1 and h2:
            rank = len(F.generators)
            neg_q = bool(n_val > 1 and rank >= 2)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: n is a positive integer",
    "¬Q: F^n is not a fully characteristic subgroup of F"
]

N_HYP = 2
NEG_Q_INDEX = 2