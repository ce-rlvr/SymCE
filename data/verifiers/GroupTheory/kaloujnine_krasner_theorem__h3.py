import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G, N, and H are groups
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isinstance(H, PermutationGroup))
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h2 = False

    # ¬Q: G is not isomorphic to a subgroup of the unrestricted wreath product of N by H
    try:
        n_ord = N.order()
        h_ord = H.order()
        g_ord = G.order()
        
        # Prevent massive computations if a ridiculously large group is provided
        if h_ord > 1000:
            neg_q = False
        else:
            # The order of the unrestricted wreath product of N by H is |N|^|H| * |H|.
            wreath_order = (n_ord ** h_ord) * h_ord
            
            # By Lagrange's Theorem, a necessary condition for G to be isomorphic 
            # to a subgroup of N wr H is that |G| divides |N wr H|.
            # If it does not divide, G is definitely NOT a subgroup (so ¬Q is True).
            # This sound check is sufficient to verify many simple counterexamples.
            neg_q = bool(wreath_order % g_ord != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G, N, and H are groups",
    "H_2: N is a normal subgroup of G",
    "¬Q: G is not isomorphic to a subgroup of the unrestricted wreath product of N by H"
]

N_HYP = 2
NEG_Q_INDEX = 2