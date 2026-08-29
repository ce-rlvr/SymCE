import sympy
from sympy import Symbol, Poly

x = Symbol('x')

def conditions(witness) -> list[bool]:
    # Handle witness as (f, p) or just f
    if isinstance(witness, tuple) and len(witness) == 2:
        f, p = witness
    else:
        f = witness
        p = None

    # H1: R is a UFD with field of fractions K
    # We interpret this as f being a polynomial over Z, and p being a prime in Z.
    try:
        poly = Poly(f, x, domain='ZZ')
        h1_f = True
    except Exception:
        h1_f = False

    # If p is not provided, attempt to find a prime that satisfies the conditions
    if p is None and h1_f:
        try:
            coeffs = poly.all_coeffs()
            a_n = coeffs[0]
            a_0 = coeffs[-1]
            for test_p in sympy.primerange(2, 100):
                if a_n % test_p != 0:
                    if all(c % test_p == 0 for c in coeffs[1:]):
                        if a_0 % (test_p**2) != 0:
                            p = test_p
                            break
        except Exception:
            pass

    try:
        h1 = h1_f and (p is not None) and sympy.isprime(p)
    except Exception:
        h1 = False

    # H2: p \nmid a_n
    try:
        poly = Poly(f, x, domain='ZZ')
        coeffs = poly.all_coeffs()
        a_n = coeffs[0]
        h2 = (a_n % p != 0) if p is not None else False
    except Exception:
        h2 = False

    # H3: p \mid a_i for 0 <= i < n
    try:
        poly = Poly(f, x, domain='ZZ')
        coeffs = poly.all_coeffs()
        h3 = all(c % p == 0 for c in coeffs[1:]) if p is not None else False
    except Exception:
        h3 = False

    # H4: p^2 \nmid a_0
    try:
        poly = Poly(f, x, domain='ZZ')
        coeffs = poly.all_coeffs()
        a_0 = coeffs[-1]
        h4 = (a_0 % (p**2) != 0) if p is not None else False
    except Exception:
        h4 = False

    # neg_Q: f(x) is NOT irreducible over K
    try:
        poly_qq = Poly(f, x, domain='QQ')
        if poly_qq.degree() <= 0:
            # Constants (degree 0) and zero are not irreducible over a field
            is_irreducible = False
        else:
            _, factors = poly_qq.factor_list()
            # A polynomial is irreducible if it has exactly one factor of multiplicity 1
            if len(factors) == 1 and factors[0][1] == 1:
                is_irreducible = True
            else:
                is_irreducible = False
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain with field of fractions K",
    "H_2: There exists a prime element p in R such that p does not divide a_n",
    "H_3: p divides a_i for all integers i such that 0 <= i < n",
    "H_4: p^2 does not divide a_0",
    "¬Q: f(x) is not irreducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4