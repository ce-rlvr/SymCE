import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        G, K, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: K is a subgroup of G
    try:
        h2 = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h2 = False
        
    G_elems = []
    K_elems = []
    left_cosets = set()
    
    if h1 and h2:
        try:
            G_elems = list(G.generate())
            K_elems = list(K.generate())
            for g in G_elems:
                coset = frozenset([g * k for k in K_elems])
                left_cosets.add(coset)
        except Exception:
            pass

    # H_3: G acts on the set of left cosets G/K by left multiplication
    try:
        if h1 and h2 and left_cosets:
            h3 = True
            id_G = G.identity
            for c in left_cosets:
                if frozenset([id_G * x for x in c]) != c:
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: There is no natural bijection between the orbits of H on G/K and the set of double cosets H \ G / K
    try:
        if not (h1 and h2 and left_cosets):
            neg_q = False
        else:
            if hasattr(H, "generate"):
                H_elems = list(H.generate())
            else:
                H_elems = list(H)
                
            # Orbits of H on G/K
            adj = {c: set() for c in left_cosets}
            for c in left_cosets:
                for h in H_elems:
                    hc = frozenset([h * x for x in c])
                    if hc in left_cosets:
                        adj[c].add(hc)
                        adj[hc].add(c)
                        
            visited = set()
            num_orbits = 0
            for c in left_cosets:
                if c not in visited:
                    num_orbits += 1
                    queue = [c]
                    visited.add(c)
                    while queue:
                        curr = queue.pop(0)
                        for neighbor in adj[curr]:
                            if neighbor not in visited:
                                visited.add(neighbor)
                                queue.append(neighbor)
                                
            # Double cosets H \ G / K
            double_cosets = set()
            for g in G_elems:
                dc = frozenset([h * g * k for h in H_elems for k in K_elems])
                double_cosets.add(dc)
                
            num_double_cosets = len(double_cosets)
            
            neg_q = (num_orbits != num_double_cosets)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of G",
    "H_3: G acts on the set of left cosets G/K by left multiplication",
    "¬Q: There is no natural bijection between the orbits of H on G/K and the set of double cosets H \\ G / K"
]

N_HYP = 3
NEG_Q_INDEX = 3