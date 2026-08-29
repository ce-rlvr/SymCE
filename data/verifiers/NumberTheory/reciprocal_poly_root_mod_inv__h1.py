import math
from sympy import Poly, Integer
from sympy.abc import x

def conditions(witness) -> list[bool]:
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (f, r, p)
    where:
      - f is a sympy expression in x
      - r is an integer
      - p is an integer >= 2
    """
    try:
        f, r, p = witness
        if not isinstance(r, (int, Integer)):
            return [False, False, False, False]
        if not isinstance(p, (int, Integer)):
            return [False, False, False, False]
        r_int = int(r)
        p_int = int(p)
    except Exception:
        return [False, False, False, False]

    try:
        f_poly = Poly(f, x)
    except Exception:
        f_poly = None

    # H1: f(x) is a polynomial of degree d with integer coefficients
    try:
        if f_poly is not None:
            # Check that degree is >= 0 (not the zero polynomial) and all coefficients are integers
            h1 = (f_poly.degree() >= 0) and all(isinstance(c, (int, Integer)) for c in f_poly.all_coeffs())
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: r is an integer root of f(x) == 0 mod p
    try:
        if f_poly is not None and p_int >= 2:
            val = f_poly.eval(r_int)
            h2 = (int(val) % p_int == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: r is not divisible by p
    try:
        if p_int >= 2:
            h3 = (r_int % p_int != 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The modular inverse of r modulo p is a root of f*(x) == 0 mod p (Conclusion fails)
    try:
        if f_poly is not None and p_int >= 2:
            if math.gcd(r_int, p_int) != 1:
                # If r and p are not coprime, the modular inverse does not exist.
                # Thus, the statement "The modular inverse of r modulo p is a root..." is false.
                neg_q = True
            else:
                r_inv = pow(r_int, -1, p_int)
                coeffs = f_poly.all_coeffs()
                # f*(x) = sum_{i=0}^d c_{d-i} x^i
                # coeffs are [c_d, c_{d-1}, ..., c_0]
                # f*(r_inv) = c_d * r_inv^0 + c_{d-1} * r_inv^1 + ... + c_0 * r_inv^d
                f_star_val = sum(int(c) * pow(r_inv, i, p_int) for i, c in enumerate(coeffs))
                neg_q = (f_star_val % p_int != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial of degree d with integer coefficients",
    "H_2: r is an integer root of f(x) = 0 mod p",
    "H_3: r is not divisible by p",
    "¬Q: The modular inverse of r modulo p is not a root of f^*(x) = 0 mod p (or does not exist)"
]

N_HYP = 3
NEG_Q_INDEX = 3