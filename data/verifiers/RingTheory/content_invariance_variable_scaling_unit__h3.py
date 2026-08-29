import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f, u = witness
        u = sympy.sympify(u)
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(f, Poly):
            p = f
        else:
            p = Poly(sympy.sympify(f), x)
        h1 = p.domain.is_UFD
    except Exception:
        h1 = False
        
    try:
        if isinstance(f, Poly):
            p = f
        else:
            p = Poly(sympy.sympify(f), x)
        h2 = not p.is_zero
    except Exception:
        h2 = False
        
    try:
        if isinstance(f, Poly):
            expr = f.as_expr()
            domain = f.domain
            p = f
        else:
            expr = sympy.sympify(f)
            p = Poly(expr, x)
            domain = p.domain
            
        domain.to_domain(u)
        
        p_ux = Poly(expr.subs(x, u*x), x, domain=domain)
        
        c_f = p.content()
        c_f_ux = p_ux.content()
        
        if c_f == c_f_ux:
            are_assoc = True
        elif c_f == domain.zero or c_f_ux == domain.zero:
            are_assoc = False
        else:
            try:
                q1, r1 = domain.divide(c_f, c_f_ux)
                q2, r2 = domain.divide(c_f_ux, c_f)
                are_assoc = (r1 == domain.zero) and (r2 == domain.zero)
            except Exception:
                try:
                    q1 = domain.exquo(c_f, c_f_ux)
                    q2 = domain.exquo(c_f_ux, c_f)
                    are_assoc = True
                except Exception:
                    are_assoc = False
                    
        neg_q = not are_assoc
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial",
    "neg_Q: The content of f(ux) is not associate to the content of f(x) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2