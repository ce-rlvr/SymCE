import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: k(G/N) is the number of conjugacy classes of the quotient group G/N",
    "¬Q: k(G/N) > k(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        is_sub = all(g in G for g in N.generators)
        h2 = is_sub and G.is_normal(N)
    except Exception:
        h2 = False
        
    # H_3: k(G/N) is the number of conjugacy classes of the quotient group G/N
    # This is a definitional hypothesis; we just verify N is a valid group.
    try:
        h3 = isinstance(N, PermutationGroup)
    except Exception:
        h3 = False
        
    # ¬Q: k(G/N) > k(G)
    try:
        elements = list(G.generate())
        N_elements = list(N.generate())
        
        # Precompute mapping from any element in G to its left coset representative
        element_to_rep = {}
        coset_reps = []
        for x in elements:
            if x not in element_to_rep:
                coset_reps.append(x)
                for n in N_elements:
                    element_to_rep[x * n] = x
                    
        # Compute k(G/N): number of orbits of cosets under conjugation by G
        visited = set()
        k_G_N = 0
        for x in coset_reps:
            if x not in visited:
                k_G_N += 1
                orbit = set([x])
                queue = [x]
                while queue:
                    curr = queue.pop(0)
                    for g in G.generators:
                        conj = g * curr * g**-1
                        rep = element_to_rep.get(conj)
                        if rep is not None and rep not in orbit:
                            orbit.add(rep)
                            queue.append(rep)
                visited.update(orbit)
                
        # Compute k(G): number of conjugacy classes of G
        visited_G = set()
        k_G = 0
        for x in elements:
            if x not in visited_G:
                k_G += 1
                orbit = set([x])
                queue = [x]
                while queue:
                    curr = queue.pop(0)
                    for g in G.generators:
                        conj = g * curr * g**-1
                        if conj not in orbit:
                            orbit.add(conj)
                            queue.append(conj)
                visited_G.update(orbit)
                
        neg_q = k_G_N > k_G
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]