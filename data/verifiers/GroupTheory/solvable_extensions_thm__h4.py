import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            if hasattr(N, 'is_normal'):
                h2 = bool(N.is_normal(G))
            else:
                is_sub = False
                if hasattr(N, 'is_subgroup'):
                    is_sub = bool(N.is_subgroup(G))
                else:
                    is_sub = True
                    for gen in N.generators:
                        if not gen.is_Identity and gen not in G:
                            is_sub = False
                            break
                
                if is_sub:
                    h2 = True
                    for g in G.generators:
                        for n in N.generators:
                            conj = g * n * g**-1
                            if not conj.is_Identity and conj not in N:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False
        
    # H3: N is a solvable group
    try:
        h3 = bool(N.is_solvable)
    except Exception:
        h3 = False
        
    # neg_Q: G is NOT a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3