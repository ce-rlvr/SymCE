import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, f, g = witness
            elif len(witness) == 2:
                f, g = witness
                poly_f = Poly(f)
                poly_g = Poly(g)
                R = poly_f.domain.unify(poly_g.domain)
            else:
                return [False, False]
        else:
            return [False, False]

        # H1: R is a unique factorization domain
        try:
            h1 = bool(R.is_UFD)
        except Exception:
            h1 = False

        # Conclusion: The content of fg is equal to the product of the contents of f and g, up to a unit
        try:
            poly_f = Poly(f, domain=R)
            poly_g = Poly(g, domain=R)
            poly_fg = Poly(f * g, domain=R)

            def get_content(poly):
                coeffs = poly.coeffs()
                if not coeffs:
                    return R.zero
                c = coeffs[0]
                for coeff in coeffs[1:]:
                    c = R.gcd(c, coeff)
                return c

            cf = get_content(poly_f)
            cg = get_content(poly_g)
            cfg = get_content(poly_fg)

            # Product of contents
            prod_c = cf * cg

            def are_associate(a, b):
                if a == R.zero and b == R.zero:
                    return True
                if a == R.zero or b == R.zero:
                    return False
                try:
                    # Check if a divides b and b divides a in the domain R
                    R.exquo(a, b)
                    R.exquo(b, a)
                    return True
                except Exception:
                    return False

            q_holds = are_associate(cfg, prod_c)
            neg_q = not q_holds
        except Exception:
            neg_q = False

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: The content of fg is not equal to the product of the contents of f and g up to a unit in R"
]

N_HYP = 1
NEG_Q_INDEX = 1