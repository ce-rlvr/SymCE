import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, N, g, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # ¬Q: The order of the coset gN in G/N does not divide k
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            neg_q = False
        elif g not in G:
            neg_q = False
        else:
            try:
                if int(k) != k:
                    k_int = None
                else:
                    k_int = int(k)
            except Exception:
                k_int = None
                
            if k_int is None:
                neg_q = False
            else:
                m = 1
                current = g
                max_order = G.order()
                while current not in N and m <= max_order:
                    current = current * g
                    m += 1
                
                if current in N:
                    neg_q = (k_int % m != 0)
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The order of the coset gN in G/N does not divide k"
]

N_HYP = 2
NEG_Q_INDEX = 2