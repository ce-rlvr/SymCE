import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1 = True
        for n in N.generators:
            if n not in G:
                h1 = False
                break
        if h1:
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # neg_Q: The commutator subgroup of G and N is not equal to N
    try:
        if G.order() > 500:
            neg_q = False
        else:
            g_elems = list(G.generate())
            n_elems = list(N.generate())
            
            gens = []
            for g in g_elems:
                for n in n_elems:
                    gens.append(g * n * ~g * ~n)
                    
            if not gens:
                comm_GN = PermutationGroup([g_elems[0]**0])
            else:
                comm_GN = PermutationGroup(gens)
            
            is_equal = True
            for c in comm_GN.generators:
                if c not in N:
                    is_equal = False
                    break
            if is_equal:
                for n in N.generators:
                    if n not in comm_GN:
                        is_equal = False
                        break
            
            neg_q = not is_equal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The commutator subgroup of G and N is not equal to N"
]

N_HYP = 1
NEG_Q_INDEX = 1