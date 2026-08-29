import sympy
from sympy import Poly, Symbol, isprime

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Given a witness (f, p) where f is a polynomial in x and p is an integer,
    checks if it is a counterexample to the false conjecture.
    """
    try:
        f, p = witness
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H2: p does not divide the leading coefficient of f(x)
    try:
        poly_f = Poly(f, x)
        lc = poly_f.LC()
        if hasattr(lc, 'is_Rational') and lc.is_Rational:
            h2_ok = (lc.p % p != 0)
        else:
            h2_ok = (int(lc) % p != 0)
    except Exception:
        h2_ok = False

    # H3: The reduction of f(x) modulo p is irreducible over Z_p
    try:
        if not h1_ok:
            h3_ok = False
        else:
            poly_f = Poly(f, x)
            new_coeffs = []
            valid_reduction = True
            for c in poly_f.all_coeffs():
                if hasattr(c, 'is_Rational') and c.is_Rational:
                    num, den = c.p, c.q
                    if den % p == 0:
                        valid_reduction = False
                        break
                    inv = pow(den, -1, p)
                    new_coeffs.append((num * inv) % p)
                else:
                    new_coeffs.append(int(c) % p)
            
            if not valid_reduction:
                h3_ok = False
            else:
                reduced_poly = Poly.from_list(new_coeffs, gens=x, modulus=p)
                # In Z_p, units (degree 0) are not irreducible.
                if reduced_poly.degree() <= 0:
                    h3_ok = False
                else:
                    h3_ok = bool(reduced_poly.is_irreducible)
    except Exception:
        h3_ok = False

    # ¬Q: f(x) is NOT irreducible over Q (i.e., it is reducible over Q)
    try:
        poly_f_Q = Poly(f, x, domain='QQ')
        neg_q_ok = not bool(poly_f_Q.is_irreducible)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p does not divide the leading coefficient of f(x)",
    "H_3: The reduction of f(x) modulo p is irreducible over Z_p",
    "not Q: f(x) is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3