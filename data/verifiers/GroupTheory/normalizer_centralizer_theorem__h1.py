import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1_ok = True
        for gen in H.generators:
            if gen not in G:
                h1_ok = False
                break
    except Exception:
        h1_ok = False
        
    # neg_Q: Conclusion fails
    try:
        g_elements = list(G.generate())
        h_gens = H.generators
        
        # Compute C_G(H)
        c_elements = []
        for g in g_elements:
            if all(g * h == h * g for h in h_gens):
                c_elements.append(g)
        C = PermutationGroup(c_elements)
        
        # Compute N_G(H)
        n_elements = []
        for g in g_elements:
            if all((g * h * ~g) in H for h in h_gens):
                n_elements.append(g)
        N = PermutationGroup(n_elements)
        
        q_ok = True
        
        # Check if C_G(H) is normal in N_G(H)
        for n in N.generators:
            for c in C.generators:
                if (n * c * ~n) not in C:
                    q_ok = False
                    break
            if not q_ok:
                break
                
        # Check if N_G(H)/C_G(H) is isomorphic to a subgroup of Aut(H)
        if q_ok:
            maps = set()
            for n in n_elements:
                mapping = tuple(n * h * ~n for h in h_gens)
                maps.add(mapping)
            # The number of distinct conjugation automorphisms induced by N_G(H) on H
            # must equal the index of C_G(H) in N_G(H) for the isomorphism to hold.
            if len(maps) * C.order() != N.order():
                q_ok = False
                
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: C_G(H) is not a normal subgroup of N_G(H), or N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1