import sympy
from sympy import Poly, RootOf
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

def conditions(witness):
    try:
        f1_expr, f2_expr = witness
        f1 = Poly(f1_expr, x, domain='QQ')
        f2 = Poly(f2_expr, x, domain='QQ')

        if not f1.is_irreducible:
            h1 = False
        else:
            n_real1 = len(sympy.real_roots(f1))
            if 0 < n_real1 < f1.degree():
                h1 = False
            else:
                r1 = RootOf(f1, 0)
                facs1 = sympy.factor_list(f1, extension=r1)[1]
                h1 = all(fac.degree() == 1 for fac, mult in facs1)

        h2 = f1.is_irreducible and f2.is_irreducible

        minpoly_comp, _ = primitive_element([RootOf(f1, 0), RootOf(f2, 0)], x, ex=True)
        minpoly_comp = Poly(minpoly_comp, x, domain='QQ')

        n_real_comp = len(sympy.real_roots(minpoly_comp))
        if 0 < n_real_comp < minpoly_comp.degree():
            neg_q = True
        else:
            r_comp = RootOf(minpoly_comp, 0)
            facs_comp = sympy.factor_list(minpoly_comp, extension=r_comp)[1]
            neg_q = not all(fac.degree() == 1 for fac, mult in facs_comp)

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K_1/F is a normal extension",
    "H_2: K_1 and K_2 are subfields of a common overfield L",
    "¬Q: The compositum field K_1K_2 is not a normal extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2