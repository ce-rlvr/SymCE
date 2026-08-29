import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: The quotient group G/N is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (G, N), checks if it is a valid counterexample to the false conjecture:
    "If G is an abelian group, then the quotient group G/N is an abelian group."
    (The dropped hypothesis is that N is a normal subgroup of G).
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]

    # H_1: G is an abelian group
    try:
        h1 = bool(G.is_abelian)
    except Exception:
        h1 = False

    # ¬Q: G/N is not an abelian group
    try:
        # G/N is a valid quotient group iff N is a normal subgroup of G.
        # It is an abelian group iff it is a valid quotient group AND the derived subgroup of G is in N.
        if not hasattr(N, 'generators') or not hasattr(G, '__contains__'):
            q = False
        elif not all(g in G for g in N.generators):
            q = False
        elif not G.is_normal(N):
            q = False
        else:
            D = G.derived_subgroup()
            q = all(d in N for d in D.generators)
    except Exception:
        # If any check fails (e.g., N is not a group), G/N is not an abelian group.
        q = False

    neg_q = not q

    return [h1, neg_q]