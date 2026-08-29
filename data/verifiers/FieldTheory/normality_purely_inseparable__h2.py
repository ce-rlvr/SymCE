import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    """
    witness: A SymPy expression representing a primitive element of the extension K/QQ.
             It can be a polynomial in `x` (e.g., x**3 - 2) representing the minimal polynomial,
             or an algebraic number (e.g., sympy.cbrt(2)).
    """
    try:
        if hasattr(witness, 'free_symbols') and not witness.free_symbols:
            poly_expr = sympy.minpoly(witness, x)
            p = Poly(poly_expr, x, domain='QQ')
        else:
            p = Poly(witness, x, domain='QQ')
            
        h1 = bool(p.degree() > 0 and p.is_irreducible)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'free_symbols') and not witness.free_symbols:
            poly_expr = sympy.minpoly(witness, x)
            p = Poly(poly_expr, x, domain='QQ')
        else:
            p = Poly(witness, x, domain='QQ')
            
        if p.degree() <= 1:
            is_normal = True
        else:
            n_roots = p.nroots()
            real_roots = []
            complex_roots = []
            for r in n_roots:
                try:
                    if abs(complex(r).imag) < 1e-9:
                        real_roots.append(r)
                    else:
                        complex_roots.append(r)
                except Exception:
                    pass
            
            if len(real_roots) > 0 and len(complex_roots) > 0:
                is_normal = False
            elif p.degree() == 2:
                is_normal = True
            elif p.degree() == 3:
                is_normal = bool(sympy.sqrt(p.discriminant()).is_rational)
            else:
                try:
                    alpha = sympy.RootOf(p, 0)
                    factors = sympy.factor_list(p, extension=alpha)
                    is_normal = all(f.degree() == 1 for f, _ in factors[1])
                except Exception:
                    is_normal = True
                    
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K/F is an algebraic field extension",
    "¬Q: K/F is not a normal extension"
]

N_HYP = 1
NEG_Q_INDEX = 1