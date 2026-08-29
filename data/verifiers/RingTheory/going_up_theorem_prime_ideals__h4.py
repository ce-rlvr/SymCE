import sympy
from sympy import I, re, im
from sympy.ntheory import isprime
import math

# Top-level setup
Z = 'Z'
Z_i = 'Z[i]'

def is_prime_ideal_Z(n):
    if n == 0:
        return True
    return isprime(abs(n))

def is_gaussian_prime_ideal(q):
    if q == 0:
        return True
    a, b = int(re(q)), int(im(q))
    norm = a**2 + b**2
    if isprime(norm):
        return True
    if a == 0 and isprime(abs(b)) and abs(b) % 4 == 3:
        return True
    if b == 0 and isprime(abs(a)) and abs(a) % 4 == 3:
        return True
    return False

def intersection_Z(q, S):
    if S == 'Z':
        return abs(q)
    elif S == 'Z[i]':
        if q == 0:
            return 0
        a, b = int(re(q)), int(im(q))
        return (a**2 + b**2) // math.gcd(a, b)
    return None

def subset_ideal(q1, q2, S):
    if q2 == 0:
        return q1 == 0
    if S == 'Z':
        return q1 % q2 == 0
    elif S == 'Z[i]':
        a, b = int(re(q1)), int(im(q1))
        c, d = int(re(q2)), int(im(q2))
        norm = c**2 + d**2
        real_part = a*c + b*d
        imag_part = b*c - a*d
        return real_part % norm == 0 and imag_part % norm == 0
    return False

def get_prime_ideals_above(p, S):
    if not is_prime_ideal_Z(p):
        return []
    p = abs(p)
    if p == 0:
        return [0]
    if S == 'Z':
        return [p]
    elif S == 'Z[i]':
        if p == 2:
            return [1 + I]
        elif p % 4 == 3:
            return [p]
        elif p % 4 == 1:
            for a in range(1, int(math.sqrt(p)) + 1):
                b2 = p - a**2
                b = int(math.sqrt(b2))
                if b**2 == b2:
                    return [a + b*I, a - b*I]
    return []

def exists_Q2(Q1, P2, S):
    candidates = get_prime_ideals_above(P2, S)
    for Q2 in candidates:
        if subset_ideal(Q1, Q2, S):
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        S = witness['S']
        P1 = witness['P1']
        P2 = witness['P2']
        Q1 = witness['Q1']
    except Exception:
        return [False] * 4 + [False]

    # H1: R and S are commutative rings with identity
    try:
        h1 = (R in ['Z', 'Z[i]']) and (S in ['Z', 'Z[i]'])
    except Exception:
        h1 = False

    # H2: R is a subring of S
    try:
        if R == 'Z' and S in ['Z', 'Z[i]']:
            h2 = True
        elif R == 'Z[i]' and S == 'Z[i]':
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: S is an integral extension of R
    try:
        if R == 'Z' and S in ['Z', 'Z[i]']:
            h3 = True
        elif R == 'Z[i]' and S == 'Z[i]':
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: Q1 is a prime ideal of S such that the intersection of Q1 and R is equal to P1
    try:
        if S == 'Z':
            is_prime = is_prime_ideal_Z(Q1)
        elif S == 'Z[i]':
            is_prime = is_gaussian_prime_ideal(Q1)
        else:
            is_prime = False
        
        if not is_prime:
            h4 = False
        else:
            if R == 'Z':
                inter = intersection_Z(Q1, S)
                h4 = (inter == abs(P1))
            elif R == 'Z[i]' and S == 'Z[i]':
                h4 = subset_ideal(Q1, P1, 'Z[i]') and subset_ideal(P1, Q1, 'Z[i]')
            else:
                h4 = False
    except Exception:
        h4 = False

    # neg_Q: There does NOT exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and Q2 \cap R = P2
    try:
        if R == 'Z':
            exists = exists_Q2(Q1, P2, S)
        elif R == 'Z[i]' and S == 'Z[i]':
            is_prime_P2 = is_gaussian_prime_ideal(P2)
            exists = is_prime_P2 and subset_ideal(Q1, P2, 'Z[i]')
        else:
            exists = False
        neg_q = not exists
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "H_4: Q1 is a prime ideal of S such that the intersection of Q1 and R is equal to P1",
    "¬Q: There does not exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and the intersection of Q2 and R is equal to P2"
]

N_HYP = 4
NEG_Q_INDEX = 4