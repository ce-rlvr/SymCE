import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        G, N = witness
        if isinstance(N, PermutationGroup):
            N_set = set(N.elements)
        else:
            N_set = set(N)
            
        is_subset = True
        for n in N_set:
            try:
                if not G.contains(n):
                    is_subset = False
                    break
            except Exception:
                is_subset = False
                break
                
        if not is_subset:
            q = False
        else:
            q = True
            for n in N_set:
                for g in G.generators:
                    if g * n * ~g not in N_set:
                        q = False
                        break
                if not q:
                    break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: N is not a disjoint union of conjugacy classes of G"
]

N_HYP = 1
NEG_Q_INDEX = 1