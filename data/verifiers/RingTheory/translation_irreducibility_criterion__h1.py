import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f_in, c = witness
                f = sympy.Poly(f_in)
            elif len(witness) == 3:
                f_in, c, x_sym = witness
                f = sympy.Poly(f_in, x_sym)
            elif len(witness) == 4:
                f_in, c, x_sym, domain = witness
                f = sympy.Poly(f_in, x_sym, domain=domain)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if len(f.gens) != 1:
            return [False, False, False, False]
        x_var = f.gens[0]
        domain = f.domain
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(f, sympy.Poly)
    except Exception:
        h1 = False

    try:
        if hasattr(domain, '__contains__'):
            h2 = c in domain
        else:
            h2 = True
    except Exception:
        h2 = False

    try:
        if hasattr(domain, 'to_sympy'):
            try:
                c_expr = domain.to_sympy(c)
            except Exception:
                c_expr = sympy.sympify(c)
        else:
            c_expr = sympy.sympify(c)
            
        f_shifted = sympy.Poly(f.as_expr().subs(x_var, x_var + c_expr), x_var, domain=domain)
        h3 = (f_shifted.is_irreducible is True)
    except Exception:
        h3 = False

    try:
        neg_q = (f.is_irreducible is False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: f is a polynomial", "H_2: c is in F", "H_3: f shifted is irreducible", "\u00acQ: f is not irreducible"]
N_HYP = 3
NEG_Q_INDEX = 3