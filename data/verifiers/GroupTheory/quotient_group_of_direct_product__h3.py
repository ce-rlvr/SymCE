import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

CONDITION_LABELS = [
    "H_1: G_1 and G_2 are groups",
    "H_2: N_1 is a normal subgroup of G_1",
    "¬Q: N_1 x N_2 is not a normal subgroup of G_1 x G_2, or the quotient group is not isomorphic to (G_1/N_1) x (G_2/N_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    # H1: G1 and G2 are groups
    try:
        h1 = isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N1 is a normal subgroup of G1
    try:
        h2 = isinstance(N1, PermutationGroup) and N1.is_subgroup(G1) and N1.is_normal(G1)
    except Exception:
        h2 = False

    # neg_Q: N1 x N2 is NOT a normal subgroup of G1 x G2, OR quotient is not isomorphic
    try:
        if not isinstance(N2, PermutationGroup):
            neg_q = True
        elif not N2.is_subgroup(G2):
            neg_q = True
        else:
            def embed_direct_product(H1, H2, G1, G2):
                gens = []
                d1 = G1.degree
                d2 = G2.degree
                total = d1 + d2
                
                for g in H1.generators:
                    arr = g.array_form
                    if len(arr) < d1:
                        arr = arr + list(range(len(arr), d1))
                    arr = arr + list(range(d1, total))
                    gens.append(Permutation(arr))
                    
                for g in H2.generators:
                    arr = g.array_form
                    if len(arr) < d2:
                        arr = arr + list(range(len(arr), d2))
                    arr = list(range(d1)) + [p + d1 for p in arr]
                    gens.append(Permutation(arr))
                    
                if not gens:
                    return PermutationGroup([Permutation(list(range(total)))])
                    
                return PermutationGroup(gens)

            G1xG2 = embed_direct_product(G1, G2, G1, G2)
            N1xN2 = embed_direct_product(N1, N2, G1, G2)
            
            if not N1xN2.is_subgroup(G1xG2):
                neg_q = True
            elif not N1xN2.is_normal(G1xG2):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]