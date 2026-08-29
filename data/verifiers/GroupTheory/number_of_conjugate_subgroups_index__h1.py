import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    try:
        if G.order() > 2000:
            return [h1, False]
            
        orbit = []
        for g in G.generate():
            conj_gens = [g * h * ~g for h in H.generators]
            conj_sub = PermutationGroup(conj_gens)
            if conj_sub not in orbit:
                orbit.append(conj_sub)
                
        num_conjugates = len(orbit)
        
        norm_elements_count = 0
        for g in G.generate():
            is_norm = True
            for h in H.generators:
                if (g * h * ~g) not in H:
                    is_norm = False
                    break
            if is_norm:
                norm_elements_count += 1
                
        index = G.order() // norm_elements_count
        
        q = (num_conjugates == index)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: The number of distinct conjugate subgroups of H in G is NOT equal to the index of N_G(H) in G"
]

N_HYP = 1
NEG_Q_INDEX = 1