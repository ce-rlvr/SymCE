import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime
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

def conditions(witness) -> list[bool]:
    try:
        n, p, G = witness
    except Exception:
        return [False, False, False]
    
    # H_1: n is a positive integer
    try:
        h1 = int(n) == n and n > 0
    except Exception:
        h1 = False
        
    # H_2: p is an odd prime dividing n
    try:
        h2 = int(p) == p and isprime(p) and p % 2 != 0 and n % p == 0
    except Exception:
        h2 = False
        
    # ¬Q: Every Sylow p-subgroup of G is cyclic and normal in G (must FAIL)
    try:
        # Find a Sylow p-subgroup
        P = G.sylow_subgroup(p)
        
        # Check if P is cyclic
        o = P.order() if callable(P.order) else P.order
        is_cyc = False
        if o == 1:
            is_cyc = True
        elif P.is_abelian:
            for g in P.elements:
                g_o = g.order() if callable(g.order) else g.order
                if g_o == o:
                    is_cyc = True
                    break
                    
        # Check if P is normal in G
        is_norm = True
        for g in G.generators:
            for h in P.generators:
                conj1 = g * h * ~g
                conj2 = ~g * h * g
                if not P.contains(conj1):
                    is_norm = False
                    break
                if not P.contains(conj2):
                    is_norm = False
                    break
            if not is_norm:
                break
                
        # The conclusion is that P is cyclic AND normal.
        # So neg_Q is True if P is NOT cyclic OR NOT normal.
        neg_q = not (is_cyc and is_norm)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p is an odd prime dividing n",
    "¬Q: Some Sylow p-subgroup of G is not cyclic or not normal in G"
]

N_HYP = 2
NEG_Q_INDEX = 2