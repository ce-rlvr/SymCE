import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def min_generators(G):
    if G.order() == 1:
        return 0
        
    order = G.order()
    
    # Check rank 1 (cyclic)
    for g in G.generate():
        if g.order() == order:
            return 1
            
    if len(G.generators) <= 2:
        return 2
        
    # Check rank 2
    elements = list(G.generate())
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            if PermutationGroup(elements[i], elements[j]).order() == order:
                return 2
                
    if len(G.generators) <= 3:
        return 3
        
    # Check rank 3
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            for k in range(j + 1, len(elements)):
                if PermutationGroup(elements[i], elements[j], elements[k]).order() == order:
                    return 3
                    
    return len(G.generators)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = isinstance(H, PermutationGroup)
    except Exception:
        h2_ok = False
        
    h3_ok = True
    
    try:
        rank_G = min_generators(G)
        rank_H = min_generators(H)
        
        try:
            GH = G * H
        except Exception:
            # Fallback for direct product if * operator is not supported
            gens = []
            degG = G.degree
            degH = H.degree
            for g in G.generators:
                arr = [g(i) for i in range(degG)] + [i + degG for i in range(degH)]
                gens.append(Permutation(arr))
            for h in H.generators:
                arr = [i for i in range(degG)] + [degG + h(i) for i in range(degH)]
                gens.append(Permutation(arr))
            GH = PermutationGroup(gens)
            
        rank_GH = min_generators(GH)
        neg_q_ok = rank_GH != rank_G + rank_H
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: H is a finitely generated group",
    "H_3: rank(K) denotes the minimum number of generators of a group K",
    "¬Q: rank(G * H) != rank(G) + rank(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3