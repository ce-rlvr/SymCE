import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        
    h1_ok = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            is_subgroup = True
            for gen in N.generators:
                if gen not in G:
                    is_subgroup = False
                    break
            
            if is_subgroup:
                if G.order() > 1 and G.order() == G.derived_subgroup().order():
                    elements = list(G.generate())
                    seen = set()
                    has_abelian_normal = False
                    
                    for x in elements:
                        if x in seen:
                            continue
                        if x.is_Identity:
                            seen.add(x)
                            continue
                            
                        conj_class = set()
                        for g in elements:
                            conj_class.add(g * x * ~g)
                            
                        seen.update(conj_class)
                        
                        conj_list = list(conj_class)
                        is_abelian = True
                        for i in range(len(conj_list)):
                            for j in range(i + 1, len(conj_list)):
                                if conj_list[i] * conj_list[j] != conj_list[j] * conj_list[i]:
                                    is_abelian = False
                                    break
                            if not is_abelian:
                                break
                                
                        if is_abelian:
                            has_abelian_normal = True
                            break
                            
                    if not has_abelian_normal:
                        h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            elements_G = list(G.generate())
            elements_N = list(N.generate())
            
            id_perm = elements_G[0]**0 if elements_G else Permutation()
            comm_gens = []
            comm_group = PermutationGroup([id_perm])
            
            for g in elements_G:
                for n in elements_N:
                    c = g * n * ~g * ~n
                    if c not in comm_group:
                        comm_gens.append(c)
                        comm_group = PermutationGroup(comm_gens)
            
            is_eq = True
            if comm_group.order() != N.order():
                is_eq = False
            else:
                for gen in comm_group.generators:
                    if gen not in N:
                        is_eq = False
                        break
                if is_eq:
                    for gen in N.generators:
                        if gen not in comm_group:
                            is_eq = False
                            break
                            
            neg_q_ok = not is_eq
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: The commutator subgroup of G and N is not equal to N"
]

N_HYP = 1
NEG_Q_INDEX = 1