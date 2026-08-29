import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False]
        G, N, H = witness
        
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            h1 = True
            for n in N.generators:
                if not G.contains(n):
                    h1 = False
                    break
            if h1:
                for h in H.generators:
                    if not G.contains(h):
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            gens = list(H.generators)
            if not gens:
                gens = [Permutation()]
            H_G = PermutationGroup(gens)
            while True:
                old_order = H_G.order()
                new_gens = list(H_G.generators)
                for g in G.generators:
                    for h in H_G.generators:
                        new_gens.append(g * h * ~g)
                H_G = PermutationGroup(new_gens)
                if H_G.order() == old_order:
                    break
            
            N_elems = list(N.generate())
            H_elems = list(H.generate())
            comm_gens = []
            for n in N_elems:
                for h in H_elems:
                    comm_gens.append(n * h * ~n * ~h)
            if comm_gens:
                C = PermutationGroup(comm_gens)
            else:
                C = PermutationGroup([Permutation()])
                
            is_sdp = True
            
            if C.order() * H.order() != H_G.order():
                is_sdp = False
            else:
                for h in H.generate():
                    if not h.is_Identity and C.contains(h):
                        is_sdp = False
                        break
                
                if is_sdp:
                    for c in C.generators:
                        for g in H_G.generators:
                            if not C.contains(g * c * ~g):
                                is_sdp = False
                                break
                                
            neg_q = not is_sdp
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Witness is a tuple (G, N, H) of permutation groups, with N and H subgroups of G",
    "not Q: H^G is NOT the internal semidirect product of commutator(N, H) and H"
]

N_HYP = 1
NEG_Q_INDEX = 1