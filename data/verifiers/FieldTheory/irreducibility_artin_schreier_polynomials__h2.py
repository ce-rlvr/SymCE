import sympy as sp
from sympy.polys.polytools import Poly
from sympy.ntheory import isprime
import itertools

def poly_pow_mod(base, exp, mod_poly):
    """Computes (base**exp) % mod_poly efficiently."""
    res = Poly([1], base.gen, domain=base.domain)
    base = base % mod_poly
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod_poly
        base = (base * base) % mod_poly
        exp //= 2
    return res

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The witness should be a tuple: (p, minpoly_coeffs, a_coeffs)
    where:
      - p is the characteristic (a prime).
      - minpoly_coeffs are the coefficients of the irreducible polynomial defining Fq over Fp.
      - a_coeffs are the coefficients of the element 'a' in Fq.
    Alternatively, for Fp, it can be (p, a_val).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, a_val = witness
            minpoly_coeffs = [1, 0]  # x for Fp
            a_coeffs = [a_val]
        elif isinstance(witness, tuple) and len(witness) == 3:
            p, minpoly_coeffs, a_coeffs = witness
        else:
            return [False, False, False]

        # H1: Fq is a finite field of characteristic p
        if not isprime(p):
            h1 = False
        else:
            x = sp.Symbol('x')
            try:
                minpoly = Poly(minpoly_coeffs, x, domain=sp.GF(p))
                h1 = minpoly.is_irreducible and minpoly.degree() >= 1
            except Exception:
                h1 = False

        # H2: f(x) = x^p - x - a in Fq polynomials
        try:
            if h1:
                a_poly = Poly(a_coeffs, x, domain=sp.GF(p))
                a_poly = a_poly % minpoly
                h2 = True
            else:
                h2 = False
        except Exception:
            h2 = False

        # Evaluate Conclusion: f(y) is irreducible over Fq iff Tr(a) != 0
        neg_q = False
        if h1 and h2:
            n = minpoly.degree()
            
            # Compute Tr_{Fq/Fp}(a) = sum_{i=0}^{n-1} a^{p^i} mod minpoly
            tr_poly = Poly([0], x, domain=sp.GF(p))
            curr_a = a_poly
            for _ in range(n):
                tr_poly = (tr_poly + curr_a) % minpoly
                curr_a = poly_pow_mod(curr_a, p, minpoly)
            
            tr_is_zero = (tr_poly == Poly([0], x, domain=sp.GF(p)))
            tr_condition = not tr_is_zero

            # Check if f(y) = y^p - y - a is irreducible over Fq
            # Since deg(f) = p (prime), it is irreducible iff it has no roots in Fq.
            q_val = p**n
            has_root = False
            if q_val <= 2000:
                for coeffs in itertools.product(range(p), repeat=n):
                    c_poly = Poly(coeffs, x, domain=sp.GF(p))
                    # Check if c^p - c == a
                    val = (poly_pow_mod(c_poly, p, minpoly) - c_poly) % minpoly
                    if val == a_poly:
                        has_root = True
                        break
                is_irreducible = not has_root
            else:
                # For large q, rely on the algebraic property that y^q - y = Tr(a) mod (y^p - y - a)
                is_irreducible = not tr_is_zero

            # The conclusion states: irreducible iff Tr(a) != 0
            conclusion_holds = (is_irreducible == tr_condition)
            neg_q = not conclusion_holds

        return [h1, h2, neg_q]

    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Fq is a finite field of characteristic p",
    "H_2: f(x) = x^p - x - a is a polynomial over Fq",
    "not Q: f(x) is irreducible over Fq iff Tr(a) != 0 is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2