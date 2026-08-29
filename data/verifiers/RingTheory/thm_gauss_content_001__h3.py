import sympy
from sympy import Symbol, Poly
from sympy.abc import x, y, z

X = Symbol('X')

def conditions(witness):
    try:
        if len(witness) == 3:
            f, g, h = witness
        elif len(witness) == 4:
            _, f, g, h = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        gens = set()
        for expr in (f, g, h):
            if hasattr(expr, 'free_symbols'):
                gens.update(expr.free_symbols)
        if len(gens) == 1:
            gen = list(gens)[0]
        elif X in gens:
            gen = X
        elif x in gens:
            gen = x
        elif len(gens) > 0:
            gen = list(gens)[0]
        else:
            gen = X
    except Exception:
        gen = X

    try:
        h1_ok = True
        for expr in (f, g, h):
            p = Poly(expr, gen)
            if not getattr(p.domain, 'is_UFD', False):
                h1_ok = False
                break
    except Exception:
        h1_ok = False
        
    try:
        p_f = Poly(f, gen)
        cont_f, _ = p_f.primitive()
        if p_f.domain.is_Field:
            h2_ok = (cont_f != 0)
        else:
            h2_ok = (cont_f == 1 or cont_f == -1)
    except Exception:
        h2_ok = False
        
    try:
        def is_prim(expr):
            p = Poly(expr, gen)
            cont, _ = p.primitive()
            if p.domain.is_Field:
                return cont != 0
            else:
                return cont == 1 or cont == -1
                
        neg_q_ok = not (is_prim(g) and is_prim(h))
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a primitive polynomial over R",
    "¬Q: It is not the case that both g and h are primitive polynomials over R"
]

N_HYP = 2
NEG_Q_INDEX = 2