import sympy
from sympy import Poly, QQ, ZZ, RR, CC
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        F = witness[0]
        p = witness[1]
        f = witness[2]
        if len(witness) >= 4:
            if isinstance(witness[3], (list, tuple)):
                p_factors = witness[3]
            else:
                p_factors = witness[3:]
        else:
            p_factors = None
    except Exception:
        return [False, False, False, False]

    try:
        gens = set()
        for expr in [p, f]:
            if hasattr(expr, 'free_symbols'):
                gens.update(expr.free_symbols)
        if p_factors is not None:
            for expr in p_factors:
                if hasattr(expr, 'free_symbols'):
                    gens.update(expr.free_symbols)
        if len(gens) >= 1:
            gen = sorted(list(gens), key=lambda s: s.name)[0]
        else:
            gen = x
    except Exception:
        gen = x

    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        P_p = Poly(p, gen, domain=F)
        h2 = bool(P_p.degree() >= 1)
    except Exception:
        h2 = False

    try:
        P_f = Poly(f, gen, domain=F)
        h3 = True
    except Exception:
        h3 = False

    try:
        P_p = Poly(p, gen, domain=F)
        P_f = Poly(f, gen, domain=F)
        
        factors = P_p.factor_list()
        is_nilp = True
        for factor, mult in factors[1]:
            rem = P_f % Poly(factor, gen, domain=F)
            if not rem.is_zero:
                is_nilp = False
                break
        
        if p_factors is not None:
            prod = Poly(1, gen, domain=F)
            for factor in p_factors:
                prod = prod * Poly(factor, gen, domain=F)
        else:
            prod = P_p
            
        rem_prod = P_f % prod
        prod_div = bool(rem_prod.is_zero)
        
        neg_q = bool(is_nilp != prod_div)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "H_2: p is non-constant", "H_3: f is a polynomial", "not_Q: conclusion fails"]

N_HYP = 3
NEG_Q_INDEX = 3