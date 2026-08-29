import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False, False, False]
        G, p, P, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup) or not isinstance(G, PermutationGroup):
            h3 = False
        else:
            p_int = int(p)
            if p_int <= 1 or p_int != p:
                h3 = False
            else:
                # Check if P is a subgroup of G
                p_is_sub = all(g in G for g in P.generators)
                
                # Check if order of P is the highest power of p dividing order of G
                p_order = P.order()
                g_order = G.order()
                
                k = 0
                temp = g_order
                while temp % p_int == 0:
                    k += 1
                    temp //= p_int
                    
                h3 = p_is_sub and (p_order == p_int**k)
    except Exception:
        h3 = False

    # neg_Q: P \cap N is NOT a Sylow p-subgroup of N
    try:
        if not isinstance(N, PermutationGroup) or not isinstance(P, PermutationGroup):
            neg_q = False
        else:
            p_int = int(p)
            if p_int <= 1 or p_int != p:
                neg_q = False
            else:
                # Calculate the expected order of a Sylow p-subgroup of N
                n_order = N.order()
                k_n = 0
                temp_n = n_order
                while temp_n % p_int == 0:
                    k_n += 1
                    temp_n //= p_int
                expected_i_order = p_int**k_n
                
                # Compute the intersection of P and N
                p_elems = set(P.generate())
                n_elems = set(N.generate())
                i_elems = p_elems.intersection(n_elems)
                i_order = len(i_elems)
                
                # The conclusion fails if the intersection's order is not the expected Sylow order
                neg_q = (i_order != expected_i_order)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P \\cap N is not a Sylow p-subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3