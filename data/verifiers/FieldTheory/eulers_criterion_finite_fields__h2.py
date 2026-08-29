import itertools
from sympy import Poly, GF, isprime
from sympy.abc import x

# Expected witness format:
# witness = (p, minpoly_coeffs, a_coeffs)
# where:
#   p is a prime integer
#   minpoly_coeffs is a list of integers representing the coefficients of an irreducible polynomial over GF(p)
#   a_coeffs is a list of integers representing the coefficients of a polynomial in GF(p)[x]

def conditions(witness) -> list[bool]:
    try:
        p, minpoly, a_poly = witness
    except Exception:
        return [False, False, False]
        
    # H1: F_q is a finite field with q elements
    try:
        if not isprime(p):
            h1 = False
        else:
            poly_m = Poly(minpoly, x, domain=GF(p))
            d = poly_m.degree()
            if d < 1 or p**d > 10000:
                h1 = False
            else:
                h1 = bool(poly_m.is_irreducible)
    except Exception:
        h1 = False

    # H2: a is a non-zero element of F_q
    try:
        if not h1:
            h2 = False
        else:
            poly_a = Poly(a_poly, x, domain=GF(p))
            rem = poly_a % poly_m
            h2 = not bool(rem.is_zero)
    except Exception:
        h2 = False

    # Conclusion: a is a square in F_q iff a^{(q-1)/2} == 1
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            poly_a = Poly(a_poly, x, domain=GF(p))
            poly_a = poly_a % poly_m
            
            d = poly_m.degree()
            q = p**d
            
            # Check if a is a square
            is_sq = False
            for coeffs in itertools.product(range(p), repeat=d):
                poly_x = Poly(coeffs, x, domain=GF(p))
                if (poly_x**2 % poly_m) == poly_a:
                    is_sq = True
                    break
            
            # Check if a^{(q-1)/2} == 1
            if (q - 1) % 2 != 0:
                # Exponent is not an integer.
                # The only way a^(non-integer) == 1 is if a == 1.
                if poly_a == Poly(1, x, domain=GF(p)):
                    right_side = True
                else:
                    right_side = False
            else:
                exp = (q - 1) // 2
                res = Poly(1, x, domain=GF(p))
                base = poly_a
                e = exp
                while e > 0:
                    if e % 2 == 1:
                        res = (res * base) % poly_m
                    base = (base * base) % poly_m
                    e //= 2
                right_side = (res == Poly(1, x, domain=GF(p)))
                
            neg_q = bool(is_sq != right_side)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: a is a non-zero element of F_q",
    "¬Q: a is a square in F_q iff a^{(q-1)/2} == 1 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2