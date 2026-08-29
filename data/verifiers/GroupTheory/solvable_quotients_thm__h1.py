import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (G, N) where G and N are PermutationGroup objects.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a solvable group
    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = True
        # Check if N is a subgroup of G
        if not all(n in G for n in N.generators):
            h2 = False
        else:
            # Check for normality: g * n * g^-1 in N for all generators
            for n in N.generators:
                for g in G.generators:
                    if (g * n * ~g) not in N:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: G/N is NOT solvable
    try:
        q = False
        # G/N is solvable iff the derived series of G eventually falls into N.
        # We check if any group in the derived series of G is a subgroup of N.
        series = G.derived_series()
        for H in series:
            if all(h in N for h in H.generators):
                q = True
                break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: N is a normal subgroup of G",
    "¬Q: G/N is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2