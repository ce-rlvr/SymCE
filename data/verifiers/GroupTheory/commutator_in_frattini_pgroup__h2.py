import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: Φ(G) is the Frattini subgroup of G",
    "¬Q: The commutator subgroup G' is not a subgroup of the Frattini subgroup Φ(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # The witness can be just a group G, or a tuple (G, p)
    if isinstance(witness, tuple) and len(witness) == 2:
        G, p = witness
    else:
        G = witness
        p = 2  # default prime if not provided
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: Φ(G) is the Frattini subgroup of G
    # This is a definitional hypothesis, so it's True as long as G is a valid group.
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False
        
    # ¬Q: G' is NOT a subgroup of Φ(G)
    try:
        G_elems = frozenset(G.generate())
        
        # Find the identity element
        identity = None
        for e in G_elems:
            if e.is_Identity:
                identity = e
                break
        if identity is None:
            identity = Permutation()
            
        # Find all subgroups by generating them from subsets
        trivial_subgroup = frozenset([identity])
        queue = [trivial_subgroup]
        seen = {trivial_subgroup}
        
        while queue:
            H_elems = queue.pop(0)
            for g in G_elems:
                if g not in H_elems:
                    gens = list(H_elems) + [g]
                    new_group = PermutationGroup(*gens)
                    new_elems = frozenset(new_group.generate())
                    if new_elems not in seen:
                        seen.add(new_elems)
                        queue.append(new_elems)
                        
        proper_subgroups = [H for H in seen if H != G_elems]
        
        # The Frattini subgroup is the intersection of all maximal subgroups
        if not proper_subgroups:
            frattini_elems = G_elems
        else:
            maximal_subgroups = []
            for M in proper_subgroups:
                is_maximal = True
                for H in proper_subgroups:
                    if M != H and M.issubset(H):
                        is_maximal = False
                        break
                if is_maximal:
                    maximal_subgroups.append(M)
                    
            frattini_elems = set(G_elems)
            for M in maximal_subgroups:
                frattini_elems = frattini_elems.intersection(M)
                
        # The commutator subgroup G'
        G_prime = G.derived_subgroup()
        G_prime_elems = frozenset(G_prime.generate())
        
        # Negated conclusion: G' is NOT a subgroup of Φ(G)
        neg_q = not G_prime_elems.issubset(frattini_elems)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]