import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False] * 5
        G, N, x, y = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and h1:
            # Check if N is a subgroup of G
            is_sub = all(h in G for h in N.generators)
            if is_sub:
                # Check if N is normal in G
                is_norm = True
                for g in G.generators:
                    for h in N.generators:
                        if (g * h * ~g) not in N:
                            is_norm = False
                            break
                        if (~g * h * g) not in N:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False

    # H_3: x is an element of G
    try:
        h3 = isinstance(x, Permutation) and x in G
    except Exception:
        h3 = False

    # H_4: y is an element of G
    try:
        h4 = isinstance(y, Permutation) and y in G
    except Exception:
        h4 = False

    # ¬Q: xN and yN are NOT conjugate in G/N
    try:
        neg_q = False
        if h1 and h2 and h3 and h4:
            are_conj = False
            # Check if there exists g in G such that g * x * g^-1 * y^-1 is in N
            for g in list(G.elements):
                if (g * x * ~g * ~y) in N:
                    are_conj = True
                    break
            neg_q = not are_conj
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: x is an element of G",
    "H_4: y is an element of G",
    "¬Q: xN and yN are not conjugate in G/N"
]

N_HYP = 4
NEG_Q_INDEX = 4