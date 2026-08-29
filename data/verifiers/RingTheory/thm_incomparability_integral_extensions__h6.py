import sympy
from sympy import Poly, div
from sympy.ntheory import isprime
from sympy.abc import x

# Top-level setup
# The witness expressions will be evaluated in a namespace containing 'x'.
# We represent the rings as R = Z and S = Z[x]/<f(x)>.
# The witness is expected to be a tuple: (f, Q1_gens, Q2_gens)
# where f is a polynomial in x, and Q1_gens, Q2_gens are lists of polynomials in x
# generating the ideals in Z[x] that correspond to Q1 and Q2 in S.

def conditions(witness):
    try:
        f, Q1_gens, Q2_gens = witness
    except Exception:
        return [False] * 6

    def is_in_ideal(poly, gens):
        try:
            if poly == 0:
                return True
            if len(gens) == 1:
                g = gens[0]
                if g == 0:
                    return poly == 0
                q, r = div(poly, g, domain='ZZ')
                return r == 0
            elif len(gens) == 2:
                if Poly(gens[0], x).is_constant():
                    p, g = gens[0], gens[1]
                elif Poly(gens[1], x).is_constant():
                    p, g = gens[1], gens[0]
                else:
                    return False
                p = int(p)
                if p == 0:
                    return False
                domain_str = 'GF(%d)' % abs(p)
                q, r = div(poly, g, domain=domain_str)
                return r == 0
            return False
        except Exception:
            return False

    def is_prime_ideal(gens):
        try:
            if len(gens) == 1:
                g = gens[0]
                if g == 0:
                    return True
                p_g = Poly(g, x, domain='ZZ')
                if p_g.content() != 1:
                    return False
                return p_g.is_irreducible
            elif len(gens) == 2:
                if Poly(gens[0], x).is_constant():
                    p, g = gens[0], gens[1]
                elif Poly(gens[1], x).is_constant():
                    p, g = gens[1], gens[0]
                else:
                    return False
                p = int(p)
                if not isprime(abs(p)):
                    return False
                domain_str = 'GF(%d)' % abs(p)
                p_g = Poly(g, x, domain=domain_str)
                return p_g.is_irreducible
            return False
        except Exception:
            return False

    # H_1: R and S are commutative rings with identity
    # R = Z and S = Z[x]/<f(x)> are commutative rings with identity if f is a valid polynomial.
    try:
        Poly(f, x)
        h1 = True
    except Exception:
        h1 = False

    # H_2: R is a subring of S
    # Z is a subring of Z[x]/<f(x)> if f has degree >= 1.
    try:
        h2 = Poly(f, x).degree() >= 1
    except Exception:
        h2 = False

    # H_3: S is an integral extension of R
    # Z[x]/<f(x)> is an integral extension of Z if f is monic.
    try:
        h3 = Poly(f, x).LC() == 1
    except Exception:
        h3 = False

    # H_4: Q_1 and Q_2 are prime ideals of S
    # They must be prime ideals in Z[x] and contain the ideal <f(x)>.
    try:
        q1_prime = is_prime_ideal(Q1_gens)
        q2_prime = is_prime_ideal(Q2_gens)
        f_in_q1 = is_in_ideal(f, Q1_gens)
        f_in_q2 = is_in_ideal(f, Q2_gens)
        h4 = bool(q1_prime and q2_prime and f_in_q1 and f_in_q2)
    except Exception:
        h4 = False

    # H_5: Q_1 is a subset of Q_2
    try:
        h5 = bool(all(is_in_ideal(g, Q2_gens) for g in Q1_gens))
    except Exception:
        h5 = False

    # neg_Q: Q_1 != Q_2
    # Since Q_1 is a subset of Q_2, they are equal iff Q_2 is a subset of Q_1.
    try:
        q2_in_q1 = all(is_in_ideal(g, Q1_gens) for g in Q2_gens)
        neg_q = not q2_in_q1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "H_4: Q_1 and Q_2 are prime ideals of S",
    "H_5: Q_1 is a subset of Q_2",
    "¬Q: Q_1 != Q_2"
]

N_HYP = 5
NEG_Q_INDEX = 5