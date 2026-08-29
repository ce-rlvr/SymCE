import sympy
from sympy import Poly
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f divides g in the polynomial ring",
    "¬Q: The content of f does not divide the content of g in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) == 3:
            R_in, f_in, g_in = witness
        elif len(witness) == 2:
            f_in, g_in = witness
            R_in = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if R_in is not None:
            R = R_in
            f = Poly(f_in, domain=R)
            g = Poly(g_in, domain=R)
        else:
            if hasattr(f_in, 'domain'):
                f = f_in
                R = f.domain
                if hasattr(g_in, 'domain'):
                    g = g_in
                else:
                    g = Poly(g_in, domain=R)
            else:
                f = Poly(f_in)
                R = f.domain
                g = Poly(g_in, domain=R)
        
        gens = list(f.gens)
        for gen in g.gens:
            if gen not in gens:
                gens.append(gen)
        if gens:
            f = Poly(f, *gens, domain=R)
            g = Poly(g, *gens, domain=R)
            
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        if f.is_zero:
            h2 = bool(g.is_zero)
        else:
            try:
                q = g.exquo(f)
                h2 = True
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    try:
        cf = f.content()
        cg = g.content()
        if cf == 0:
            divides = (cg == 0)
        else:
            try:
                R.exquo(cg, cf)
                divides = True
            except Exception:
                divides = False
                try:
                    cf_sym = R.to_sympy(cf)
                    cg_sym = R.to_sympy(cg)
                    ratio = sympy.simplify(cg_sym / cf_sym)
                    if R == sympy.ZZ and ratio.is_Integer:
                        divides = True
                    elif R == sympy.QQ and ratio.is_Rational:
                        divides = True
                    else:
                        R.from_sympy(ratio)
                        divides = True
                except Exception:
                    pass
        neg_q = not divides
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]