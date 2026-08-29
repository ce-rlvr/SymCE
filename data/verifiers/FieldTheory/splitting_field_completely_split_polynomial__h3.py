import sympy
from sympy import Poly, QQ, ZZ, I, sqrt
from sympy.abc import x

def conditions(witness):
    try:
        F, K, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a field
    try:
        h1 = hasattr(F, 'is_Field') and F.is_Field
    except Exception:
        h1 = False
        
    # H_2: f(x) is a non-constant polynomial over F
    try:
        if not isinstance(f, Poly):
            gens = list(f.free_symbols)
            if len(gens) == 1:
                f_F = Poly(f, gens[0], domain=F)
                h2 = f_F.degree() >= 1
            elif len(gens) == 0:
                h2 = False
            else:
                h2 = False
        else:
            f_F = Poly(f, domain=F)
            h2 = len(f_F.gens) == 1 and f_F.degree() >= 1
    except Exception:
        h2 = False
        
    # ¬Q: K = F iff f(x) factors completely into a product of linear polynomials over F
    try:
        A = (K == F)
        
        if not isinstance(f, Poly):
            gens = list(f.free_symbols)
            if len(gens) == 1:
                f_F = Poly(f, gens[0], domain=F)
            else:
                f_F = Poly(f, x, domain=F)
        else:
            f_F = Poly(f, domain=F)
            
        _, fact_list = f_F.factor_list()
        B = all(fact.degree() == 1 for fact, mult in fact_list)
        
        neg_q = (A != B)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-constant polynomial over F",
    "¬Q: K equals F is not equivalent to f factoring completely over F"
]

N_HYP = 2
NEG_Q_INDEX = 2