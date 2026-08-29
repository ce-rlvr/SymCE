import sympy
from sympy import Poly

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, sympy.Poly):
            poly = witness
        else:
            poly = sympy.Poly(witness, x)
        h1 = True
    except Exception:
        h1 = False

    try:
        if isinstance(witness, sympy.Poly):
            poly = witness
        else:
            poly = sympy.Poly(witness, x)
        h2 = len(poly.gens) == 1
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            if isinstance(witness, sympy.Poly):
                poly = witness
            else:
                poly = sympy.Poly(witness, x)
            
            domain = poly.domain
            coeffs = poly.all_coeffs()
            
            if not coeffs:
                a_0 = domain.zero
                higher_coeffs = []
            else:
                a_0 = coeffs[-1]
                higher_coeffs = coeffs[:-1]
                
            def is_unit(c, dom):
                if c == dom.zero:
                    return False
                if getattr(dom, 'is_Field', False):
                    return True
                try:
                    dom.exquo(dom.one, c)
                    return True
                except Exception:
                    if dom == sympy.ZZ:
                        return c in (dom.one, -dom.one)
                    return False

            def is_nilpotent(c, dom):
                if c == dom.zero:
                    return True
                if getattr(dom, 'is_Field', False) or dom == sympy.ZZ:
                    return False
                curr = c
                for _ in range(100):
                    try:
                        curr = dom.mul(curr, c)
                        if curr == dom.zero:
                            return True
                    except Exception:
                        break
                return False

            a_0_unit = is_unit(a_0, domain)
            higher_nilpotent = all(is_nilpotent(c, domain) for c in higher_coeffs)
            
            conclusion = a_0_unit and higher_nilpotent
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is a polynomial over R",
    "¬Q: a_0 is not a unit or some higher coeff is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2