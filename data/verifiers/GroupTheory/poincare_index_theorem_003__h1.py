import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        else:
            h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    try:
        n = G.order() / H.order()
        h2 = (n == int(n)) and int(n) > 0
    except Exception:
        h2 = False

    try:
        n_int = G.order() // H.order()
        n_fact = math.factorial(n_int)
        
        cosets = G.coset_transversal(H)
        image_gens = []
        
        if len(cosets) <= 200:
            for g in G.generators:
                perm = []
                for x in cosets:
                    gx = g * x
                    for i, y in enumerate(cosets):
                        if (~y * gx) in H:
                            perm.append(i)
                            break
                if perm:
                    image_gens.append(sympy.combinatorics.Permutation(perm))
        else:
            coset_map = {}
            for i, rep in enumerate(cosets):
                for h in H.elements:
                    coset_map[rep * h] = i
            for g in G.generators:
                perm = []
                for x in cosets:
                    gx = g * x
                    perm.append(coset_map[gx])
                if perm:
                    image_gens.append(sympy.combinatorics.Permutation(perm))
                    
        if not image_gens:
            core_index = 1
        else:
            ImageGroup = sympy.combinatorics.PermutationGroup(image_gens)
            core_index = ImageGroup.order()
            
        q = (n_fact % core_index == 0)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is a finite integer n",
    "¬Q: There is no normal subgroup K of G contained in H such that the index of K in G divides n factorial"
]

N_HYP = 2
NEG_Q_INDEX = 2