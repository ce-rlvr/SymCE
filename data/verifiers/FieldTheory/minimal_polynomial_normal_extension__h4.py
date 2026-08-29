import sympy
from sympy import Poly
from sympy.abc import x

QQ = sympy.QQ

def conditions(witness):
    try:
        F = witness['F']
        E = witness['E']
        alpha = witness['alpha']
        m_val = witness['m']
    except (TypeError, KeyError):
        return [False, False, False, False]

    try:
        if isinstance(m_val, sympy.Expr):
            gens = m_val.free_symbols
            gen = list(gens)[0] if len(gens) == 1 else sympy.Symbol('x')
            m = Poly(m_val, gen, domain=F)
        else:
            m = m_val
    except Exception:
        m = None

    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        h2 = False
        if F == E:
            h2 = True
        elif getattr(E, 'is_FiniteField', False) and getattr(F, 'is_FiniteField', False):
            h2 = (E.characteristic == F.characteristic)
        elif hasattr(E, 'mod') and hasattr(E, 'domain'):
            if E.domain == F:
                poly = E.mod
                poly_E = poly.set_domain(E)
                factors = poly_E.factor_list()
                h2 = True
                for fac, mult in factors[1]:
                    if fac.degree() > 1:
                        h2 = False
                        break
    except Exception:
        h2 = False

    try:
        h3 = False
        if m is not None:
            in_E = False
            try:
                a_E = E.from_sympy(alpha)
                in_E = True
            except Exception:
                try:
                    a_E = E(alpha)
                    in_E = True
                except Exception:
                    pass
            
            if in_E:
                if hasattr(m, 'domain') and m.domain == F and not m.is_zero:
                    try:
                        alpha_expr = sympy.sympify(alpha)
                        expr_val = sympy.simplify(m.as_expr().subs(m.gen, alpha_expr))
                        if expr_val == 0:
                            h3 = True
                    except Exception:
                        pass
                    
                    if not h3:
                        try:
                            val = m.eval(a_E)
                            if val == getattr(E, 'zero', 0) or val == 0:
                                h3 = True
                        except Exception:
                            pass
    except Exception:
        h3 = False

    try:
        neg_q = False
        if m is not None:
            m_E = m.set_domain(E)
            factors = m_E.factor_list()
            for fac, mult in factors[1]:
                if fac.degree() > 1:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a normal extension field of F",
    "H_3: alpha in E is an element algebraic over F",
    "not_Q: m(x) does NOT split completely into linear factors over E"
]

N_HYP = 3
NEG_Q_INDEX = 3