import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    # H_1: G is a transitive permutation group and N is a subgroup of G
    try:
        G, N = witness
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            h1 = False
        else:
            transitive = G.is_transitive() if callable(G.is_transitive) else G.is_transitive
            if not transitive:
                h1 = False
            else:
                # Check if N is a subgroup of G
                h1 = all(g in G for g in N.generators)
    except Exception:
        h1 = False

    # ¬Q: The orbits of N on the domain do not form a block system for G
    try:
        G, N = witness
        degree = max(G.degree, N.degree)
        
        # Compute the orbits of N on the combined domain
        n_orbits = N.orbits()
        orbits_N = [set(o) for o in n_orbits]
        
        covered = set()
        for o in orbits_N:
            covered.update(o)
            
        # Pad with singletons for any elements not moved by N
        for i in range(degree):
            if i not in covered:
                orbits_N.append({i})
                
        # Check if orbits_N is a block system for G
        # A block system must be preserved by all generators of G
        is_block_system = True
        for g in G.generators:
            for B in orbits_N:
                # Image of block B under generator g
                g_B = {g(x) for x in B}
                if g_B not in orbits_N:
                    is_block_system = False
                    break
            if not is_block_system:
                break
                
        neg_q = not is_block_system
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a transitive permutation group and N is a subgroup of G",
    "¬Q: The orbits of N on the domain do not form a block system for G"
]

N_HYP = 1
NEG_Q_INDEX = 1