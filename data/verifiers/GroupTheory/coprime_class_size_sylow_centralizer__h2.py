import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import math

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

def conjugacy_class_size(G, x):
    """Computes the size of the conjugacy class of x in G."""
    orbit = set([x])
    queue = [x]
    gens = G.generators
    while queue:
        curr = queue.pop(0)
        for g in gens:
            # Conjugate curr by g
            nxt = g * curr * ~g
            if nxt not in orbit:
                orbit.add(nxt)
                queue.append(nxt)
    return len(orbit)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        G, x, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: x is an element of G such that the size of the conjugacy class of x is coprime to p
    try:
        if not isinstance(x, Permutation):
            h2 = False
        elif x not in G:
            h2 = False
        else:
            p_int = int(p)
            c_size = conjugacy_class_size(G, x)
            h2 = (math.gcd(c_size, p_int) == 1)
    except Exception:
        h2 = False
        
    # Q: The centralizer C_G(x) contains a Sylow p-subgroup of G
    try:
        if not isinstance(x, Permutation) or x not in G:
            q = False
        else:
            p_int = int(p)
            if not sympy.isprime(p_int):
                # Sylow p-subgroups are only defined for primes.
                # If p is not prime, the conclusion is undefined/false.
                q = False
            else:
                c_size = conjugacy_class_size(G, x)
                # By Sylow's First Theorem, C_G(x) contains a Sylow p-subgroup of G
                # if and only if p does not divide the index [G : C_G(x)], 
                # which is exactly the size of the conjugacy class of x.
                q = (c_size % p_int != 0)
    except Exception:
        q = False
        
    neg_q = not q
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G such that the size of the conjugacy class of x is coprime to p",
    "¬Q: The centralizer C_G(x) does not contain a Sylow p-subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2