import sympy
from sympy.polys.rootoftools import RootOf
from sympy.abc import x

CONDITION_LABELS = ["H_1: E over F is a finite field extension", "H_2: The degree of E over F is n", "H_3: p is an irreducible polynomial over F", "neg_Q: p has a root in E"]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            minpoly_E, n, p = witness
        else:
            return [False, False, False, False]
            
        if hasattr(minpoly_E, 'ext') and hasattr(minpoly_E.ext, 'minpoly'):
            minpoly_E = minpoly_E.ext.minpoly
        elif hasattr(minpoly_E, 'is_number') and minpoly_E.is_number:
            minpoly_E = sympy.minpoly(minpoly_E, sympy.Symbol('x'))
            
        if isinstance(minpoly_E, sympy.Poly):
            minpoly_E = minpoly_E.as_expr()
        if isinstance(p, sympy.Poly):
            p = p.as_expr()
            
        m_vars = list(minpoly_E.free_symbols)
        m_var = m_vars[0] if m_vars else sympy.Symbol('x')
        
        p_vars = list(p.free_symbols)
        p_var = p_vars[0] if p_vars else sympy.Symbol('x')

    except Exception:
        return [False, False, False, False]

    try:
        facs = sympy.factor_list(minpoly_E, domain='QQ')
        h1 = (len(facs[1]) == 1 and facs[1][0][1] == 1 and sympy.degree(minpoly_E, gen=m_var) > 0)
    except Exception:
        h1 = False

    try:
        h2 = (sympy.degree(minpoly_E, gen=m_var) == n)
    except Exception:
        h2 = False

    try:
        facs_p = sympy.factor_list(p, domain='QQ')
        h3 = (len(facs_p[1]) == 1 and facs_p[1][0][1] == 1 and sympy.degree(p, gen=p_var) > 0)
    except Exception:
        h3 = False

    try:
        if sympy.degree(minpoly_E, gen=m_var) == 1:
            rts = sympy.roots(p, p_var)
            neg_q = len(rts) > 0
        else:
            ext_root = RootOf(minpoly_E, 0)
            facs_ext = sympy.factor_list(p, extension=ext_root)
            
            neg_q = False
            for f, mult in facs_ext[1]:
                if sympy.degree(f, gen=p_var) == 1:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]