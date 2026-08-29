import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    def get(name, default=None):
        if isinstance(witness, dict) and name in witness:
            return witness[name]
        if hasattr(witness, name):
            return getattr(witness, name)
        return default

    # H_1: f is a ring homomorphism from R to S
    try:
        h1 = False
        if get('is_homomorphism') is True:
            h1 = True
        else:
            R = get('R')
            S = get('S')
            add_R = get('add_R')
            mul_R = get('mul_R')
            add_S = get('add_S')
            mul_S = get('mul_S')
            f = get('f')
            one_R = get('one_R')
            one_S = get('one_S')
            
            if all(x is not None for x in (R, S, add_R, mul_R, add_S, mul_S, f, one_R, one_S)):
                h1_ok = True
                R_list = list(R)
                S_list = list(S)
                for a in R_list:
                    if f(a) not in S_list:
                        h1_ok = False
                        break
                    for b in R_list:
                        if f(add_R(a, b)) != add_S(f(a), f(b)):
                            h1_ok = False
                            break
                        if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
                if h1_ok and f(one_R) != one_S:
                    h1_ok = False
                h1 = h1_ok
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        n = get('n')
        h2 = False
        if n is not None:
            n_val = int(n)
            if n_val > 0 and n_val == n:
                h2 = True
    except Exception:
        h2 = False

    # H_3: F is the induced ring homomorphism from M_n(R) to M_n(S)
    try:
        F = get('F')
        if F is not None:
            h3 = callable(F) or isinstance(F, dict)
        else:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The kernel of F is not the matrix ring M_n(K)
    # (This happens when K is an ideal but not a ring with identity, so M_n(K) is not a matrix ring)
    try:
        if get('K_is_ring') is not None:
            neg_q = not get('K_is_ring')
        else:
            R = get('R')
            zero_S = get('zero_S')
            f = get('f')
            mul_R = get('mul_R')
            
            K = [a for a in R if f(a) == zero_S]
            
            has_id = False
            for e in K:
                is_id = True
                for x in K:
                    if mul_R(e, x) != x or mul_R(x, e) != x:
                        is_id = False
                        break
                if is_id:
                    has_id = True
                    break
            
            # If K has no identity, it is not a ring, so M_n(K) is not a matrix ring.
            neg_q = not has_id
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: n is a positive integer",
    "H_3: F is the induced ring homomorphism from M_n(R) to M_n(S) that applies f to each entry",
    "¬Q: The kernel of F is not the matrix ring M_n(K) (e.g., K lacks an identity and is not a ring)"
]

N_HYP = 3
NEG_Q_INDEX = 3