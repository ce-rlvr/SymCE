import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

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
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    try:
        if hasattr(H, 'generate'):
            H_set = set(H.generate())
        else:
            H_set = set(H)
            
        h_order = len(H_set)
        if h_order == 0:
            div_by_p = False
        elif G.order() % h_order != 0:
            div_by_p = False
        else:
            index = G.order() // h_order
            div_by_p = (index % p == 0)
            
        not_div_by_p = not div_by_p
        
        P = G.sylow_subgroup(p)
        P_elements = list(P.generate())
        
        contains_sylow = False
        for g in list(G.generate()):
            conj_elements = [g * elem * ~g for elem in P_elements]
            if all(elem in H_set for elem in conj_elements):
                contains_sylow = True
                break
                
        q = (contains_sylow == not_div_by_p)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a finite group", "H_2: p is a prime number", "¬Q: H contains a Sylow p-subgroup iff index is not divisible by p FAILS"]
N_HYP = 2
NEG_Q_INDEX = 2