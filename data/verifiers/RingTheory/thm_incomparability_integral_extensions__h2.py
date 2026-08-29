import sympy
import math

# Top-level setup
# We represent subrings and ideals of Z x Z as tuples of two integers (a, b),
# which stands for the set aZ x bZ.
# For example, (1, 0) represents Z x 0.
Z_x_0 = (1, 0)
Z_x_Z = (1, 1)
Z_x_2Z = (1, 2)
Z_x_3Z = (1, 3)
Z_x_5Z = (1, 5)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            Q1 = witness['Q1']
            Q2 = witness['Q2']
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            R, S, Q1, Q2 = witness
        else:
            R = witness.R
            S = witness.S
            Q1 = witness.Q1
            Q2 = witness.Q2
    except Exception:
        return [False] * 6

    def parse(X):
        if isinstance(X, (list, tuple)) and len(X) == 2:
            return (int(X[0]), int(X[1]))
        raise ValueError

    try:
        R = parse(R)
        S = parse(S)
        Q1 = parse(Q1)
        Q2 = parse(Q2)
    except Exception:
        return [False] * 6

    def divides(c, a):
        if c == 0:
            return a == 0
        return a % c == 0

    def subset(A, B):
        return divides(B[0], A[0]) and divides(B[1], A[1])

    def is_ring_with_id(X):
        return X[0] in (0, 1) and X[1] in (0, 1)

    def is_integral_extension(R_ring, S_ring):
        if not subset(R_ring, S_ring):
            return False
        # In our ZxZ model, if R <= S and both are rings with identity,
        # S is always an integral extension of R.
        # For any s in S, 1_R * s is in R, so P(t) = 1_R t - 1_R s is a monic
        # polynomial in R[t] that annihilates s.
        return True

    def is_zero_ring(s, q):
        return s == q

    def is_integral_domain(s, q):
        if s == 0:
            return False
        if s == 1:
            return q == 0 or sympy.isprime(q)
        return False

    def is_prime_ideal(Q, S_ring):
        if not subset(Q, S_ring):
            return False
        s1, s2 = S_ring
        q1, q2 = Q
        if is_integral_domain(s1, q1) and is_zero_ring(s2, q2):
            return True
        if is_zero_ring(s1, q1) and is_integral_domain(s2, q2):
            return True
        return False

    def lcm(a, b):
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // math.gcd(a, b)

    def intersection(A, B):
        return (lcm(A[0], B[0]), lcm(A[1], B[1]))

    try:
        h1 = is_ring_with_id(R) and is_ring_with_id(S)
    except Exception:
        h1 = False

    try:
        h2 = is_integral_extension(R, S)
    except Exception:
        h2 = False

    try:
        h3 = is_prime_ideal(Q1, S) and is_prime_ideal(Q2, S)
    except Exception:
        h3 = False

    try:
        h4 = subset(Q1, Q2)
    except Exception:
        h4 = False

    try:
        h5 = intersection(Q1, R) == intersection(Q2, R)
    except Exception:
        h5 = False

    try:
        neg_q = Q1 != Q2
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: S is an integral extension of R",
    "H_3: Q_1 and Q_2 are prime ideals of S",
    "H_4: Q_1 is a subset of Q_2",
    "H_5: Q_1 ∩ R = Q_2 ∩ R",
    "¬Q: Q_1 != Q_2"
]

N_HYP = 5
NEG_Q_INDEX = 5