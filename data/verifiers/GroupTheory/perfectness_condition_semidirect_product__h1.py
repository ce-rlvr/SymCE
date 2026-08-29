import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
        
        G_perf = (G.derived_subgroup().order() == G.order())
        H_perf = (H.derived_subgroup().order() == H.order())
        
        N_N = N.derived_subgroup()
        
        commutators = []
        for n in list(N.generate()):
            for h in list(H.generate()):
                commutators.append(n**-1 * h**-1 * n * h)
                
        id_perm = list(G.generate())[0]**0
        if not commutators:
            commutators = [id_perm]
            
        N_H = PermutationGroup(commutators)
        
        gens = list(N_H.generators) + list(N_N.generators)
        if not gens:
            gens = [id_perm]
        N_H_N_N = PermutationGroup(gens)
        
        N_cond = N_H_N_N.is_subgroup(N) and N_H_N_N.order() == N.order()
        
        Q = (G_perf == (H_perf and N_cond))
        neg_Q = not Q
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = ["~Q: The equivalence (G is perfect iff H is perfect and N = commutator(N, H) * commutator(N, N)) fails"]
N_HYP = 0
NEG_Q_INDEX = 0