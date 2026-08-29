import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup for witness expressions
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
    # The witness is expected to be a tuple: (G, p, P)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, P = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number dividing the order of G
    try:
        p_int = int(p)
        order_G = int(G.order())
        h1 = sympy.ntheory.isprime(p_int) and (order_G % p_int == 0)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        is_sub = all(g in G for g in P.generators)
        if not is_sub:
            h2 = False
        else:
            order_G = int(G.order())
            order_P = int(P.order())
            p_int = int(p)
            k = 0
            temp = order_G
            while temp > 0 and temp % p_int == 0:
                k += 1
                temp //= p_int
            h2 = (order_P == p_int**k)
    except Exception:
        h2 = False

    # H_3: P is contained in the center of its normalizer N_G(P)
    try:
        P_elements = set(P.generate())
        N_G_P_elements = []
        for g in G.generate():
            is_in_normalizer = True
            for x in P.generators:
                if g * x * ~g not in P_elements:
                    is_in_normalizer = False
                    break
            if is_in_normalizer:
                N_G_P_elements.append(g)
                
        h3 = True
        for p_elem in P.generators:
            for n_elem in N_G_P_elements:
                if p_elem * n_elem != n_elem * p_elem:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # ¬Q: G does NOT have a normal p-complement
    try:
        order_G = int(G.order())
        order_P = int(P.order())
        p_int = int(p)
        if order_P == 0 or order_G % order_P != 0:
            neg_q = True
        else:
            m = order_G // order_P
            
            # A normal p-complement must contain exactly all elements of order coprime to p.
            S = []
            for g in G.generate():
                if math.gcd(int(g.order()), p_int) == 1:
                    S.append(g)
                    
            if len(S) == m:
                S_set = set(S)
                is_subgroup = True
                for g1 in S:
                    for g2 in S:
                        if g1 * g2 not in S_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                if is_subgroup:
                    P_elements = set(P.generate())
                    intersection = P_elements.intersection(S_set)
                    if len(intersection) == 1:
                        neg_q = False  # A normal p-complement exists
                    else:
                        neg_q = True
                else:
                    neg_q = True
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: P is contained in the center of its normalizer N_G(P)",
    "¬Q: G does not have a normal p-complement"
]

N_HYP = 3
NEG_Q_INDEX = 3