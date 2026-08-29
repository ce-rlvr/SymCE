import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import primefactors

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

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False]
            
        n = witness.order()
        if n == 1:
            neg_q = False
        else:
            primes = primefactors(n)
            all_sylows = []
            elements = list(witness.elements)
            
            for p in primes:
                P = witness.sylow_subgroup(p)
                seen = set()
                for g in elements:
                    conj_gens = [~g * x * g for x in P.generators]
                    P_g = PermutationGroup(conj_gens)
                    P_g_elements = frozenset(P_g.elements)
                    if P_g_elements not in seen:
                        seen.add(P_g_elements)
                        all_sylows.append(P_g)
                        
            intersection_size = 0
            for g in elements:
                normalizes_all = True
                for S in all_sylows:
                    for x in S.generators:
                        if (~g * x * g) not in S:
                            normalizes_all = False
                            break
                    if not normalizes_all:
                        break
                if normalizes_all:
                    intersection_size += 1
                    
            neg_q = (intersection_size > 1)
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The intersection of the normalizers of all Sylow subgroups of G is not the trivial subgroup"
]

N_HYP = 0
NEG_Q_INDEX = 0