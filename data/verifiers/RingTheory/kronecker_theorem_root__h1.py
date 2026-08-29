import sympy
from sympy.abc import x

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        p_expr = witness[-1]
    else:
        p_expr = witness
        
    try:
        if isinstance(p_expr, sympy.Poly):
            p = p_expr
        else:
            p = sympy.Poly(p_expr, x)
    except Exception:
        return [False, False, False, False]
        
    try:
        if p.domain.is_Field:
            if p.degree() <= 0:
                h1 = False
            else:
                h1 = bool(p.is_irreducible)
        elif p.domain == sympy.ZZ:
            c, prim = p.primitive()
            if prim.degree() <= 0:
                h1 = bool(sympy.isprime(abs(int(c))))
            else:
                if abs(int(c)) != 1:
                    h1 = False
                else:
                    h1 = bool(prim.is_irreducible)
        else:
            if p.degree() <= 0:
                h1 = False
            else:
                h1 = bool(p.is_irreducible)
    except Exception:
        h1 = False
        
    h2 = True
    h3 = True
    
    try:
        neg_q = bool(p.degree() <= 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p(x) is an irreducible polynomial in F(x)",
    "H_2: E is the factor ring F(x)/(p(x))",
    "H_3: alpha is the coset x + (p(x)) in E",
    "¬Q: alpha is not a root of p(x) in E"
]

N_HYP = 3
NEG_Q_INDEX = 3