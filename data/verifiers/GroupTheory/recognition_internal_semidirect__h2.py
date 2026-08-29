import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
# Klein four-group as a subgroup of S4
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G (and N is a subgroup of G)
    try:
        h2 = (isinstance(H, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              all(g in G for g in H.generators) and 
              all(g in G for g in N.generators))
    except Exception:
        h2 = False

    def get_order(grp):
        order = grp.order
        return order() if callable(order) else order

    # H_3: G = NH
    try:
        count_h3 = sum(1 for g in N.generate() if g in H)
        h3 = (get_order(G) == (get_order(N) * get_order(H)) // count_h3)
    except Exception:
        h3 = False

    # H_4: N \cap H = {e}
    try:
        count_h4 = sum(1 for g in N.generate() if g in H)
        h4 = (count_h4 == 1)
    except Exception:
        h4 = False

    # neg_Q: The conclusion fails.
    # The conclusion states G is isomorphic to N \rtimes_\phi H where \phi is conjugation.
    # This requires \phi to be well-defined, meaning H normalizes N.
    # Since G = NH, H normalizes N iff G normalizes N iff N is normal in G.
    # If N is normal in G, the theorem holds.
    # So the conclusion fails iff N is NOT normal in G.
    try:
        def is_normal_subgroup(subgroup, group):
            for g in group.generators:
                g_inv = ~g
                for n in subgroup.generators:
                    if (g * n * g_inv) not in subgroup:
                        return False
            return True
        
        neg_q = not is_normal_subgroup(N, G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G (and N is a subgroup of G)",
    "H_3: G = NH",
    "H_4: N \\cap H = \\{e\\}",
    "¬Q: G is not isomorphic to N \\rtimes_\\phi H (conjugation \\phi is not well-defined)"
]

N_HYP = 4
NEG_Q_INDEX = 4