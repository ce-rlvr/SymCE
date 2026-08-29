import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "¬Q: k(G) > k(N) k(G/N)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup):
            h2 = False
        else:
            h2 = True
            # Check if N is a subgroup of G
            for gen in N.generators:
                if gen not in G:
                    h2 = False
                    break
            # Check normality: g * n * g^-1 in N for all generators
            if h2:
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # neg_Q: k(G) > k(N) * k(G/N)
    try:
        if h1 and h2:
            def get_k(group):
                cc = group.conjugacy_classes
                if callable(cc):
                    return len(cc())
                return len(cc)
                
            k_G = get_k(G)
            k_N = get_k(N)
            
            # Compute k(G/N)
            N_elements = list(N.elements)
            def coset_id(g):
                # Canonical identifier for the coset gN
                return tuple(min((g * n).array_form for n in N_elements))
                
            id_to_rep = {}
            for g in G.elements:
                cid = coset_id(g)
                if cid not in id_to_rep:
                    id_to_rep[cid] = g
                    
            visited = set()
            k_G_N = 0
            
            # Find orbits of G/N under conjugation by G
            for cid, rep in id_to_rep.items():
                if cid not in visited:
                    k_G_N += 1
                    orbit = set([cid])
                    queue = [rep]
                    while queue:
                        curr = queue.pop(0)
                        for x in G.generators:
                            conj = x * curr * ~x
                            conj_cid = coset_id(conj)
                            if conj_cid not in orbit:
                                orbit.add(conj_cid)
                                visited.add(conj_cid)
                                queue.append(conj)
                    visited.update(orbit)
                    
            neg_q = k_G > k_N * k_G_N
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]