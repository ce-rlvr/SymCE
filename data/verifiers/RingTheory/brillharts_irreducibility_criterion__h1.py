import sympy
from sympy import Poly, isprime
from sympy.abc import x

def conditions(witness):
    # The witness can be either a tuple (f, b) or just the polynomial f.
    if isinstance(witness, tuple):
        if len(witness) == 2:
            f, b = witness
        else:
            return [False, False, False]
    else:
        f = witness
        b = None

    # Ensure f is a polynomial in x
    try:
        f_poly = Poly(f, x)
        coeffs = f_poly.all_coeffs()
    except Exception:
        return [False, False, False]

    # If b is not provided, try to find one that satisfies the conditions
    if b is None:
        try:
            if any(c < 0 for c in coeffs):
                b_min = 2
            else:
                b_min = 2
                for c in coeffs:
                    if c >= b_min:
                        b_min = int(c) + 1
            
            b_min = int(b_min)
            found_b = False
            for test_b in range(b_min, b_min + 1000):
                val = f_poly.eval(test_b)
                try:
                    if int(val) == val and isprime(int(val)):
                        b = test_b
                        found_b = True
                        break
                except TypeError:
                    pass
            if not found_b:
                b = b_min
        except Exception:
            b = 2

    # H_1: There exists an integer b >= 2 such that f(b) is a prime number
    try:
        val = f_poly.eval(b)
        h1 = (b >= 2) and (int(val) == val) and isprime(int(val))
    except Exception:
        h1 = False

    # H_2: For all 0 <= i <= n, the coefficients satisfy 0 <= a_i < b
    try:
        h2 = all(0 <= c < b for c in coeffs)
    except Exception:
        h2 = False

    # ¬Q: f(x) is NOT irreducible over Q
    try:
        # A polynomial is irreducible over Q if it has degree >= 1 and cannot be factored
        # into lower degree polynomials over Q. Constants (degree <= 0) are units or zero,
        # hence not irreducible.
        if f_poly.degree() <= 0:
            neg_q = True
        else:
            _, factors = sympy.factor_list(f, domain='QQ')
            # It is irreducible if there is exactly one factor, and its multiplicity is 1
            is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
            neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: There exists an integer b >= 2 such that f(b) is a prime number",
    "H_2: For all 0 <= i <= n, the coefficients satisfy 0 <= a_i < b",
    "¬Q: f(x) is not irreducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2