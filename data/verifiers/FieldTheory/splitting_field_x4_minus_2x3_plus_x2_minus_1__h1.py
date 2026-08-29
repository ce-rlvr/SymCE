import sympy
from sympy import Poly, sqrt

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    try:
        w = sympy.sympify(witness)
    except Exception:
        return [False, False]
        
    # H_1: f(x) is a polynomial over Q
    # The hypothesis states "K is the splitting field of f(x) over Q", 
    # which implicitly requires the witness f(x) to be a polynomial over Q.
    try:
        syms = list(w.free_symbols)
        if len(syms) > 1:
            h1_ok = False
        else:
            sym = syms[0] if syms else sympy.Symbol('x')
            p = Poly(w, sym)
            h1_ok = p.domain.is_QQ or p.domain.is_ZZ
    except Exception:
        h1_ok = False

    # neg_Q: K != Q(sqrt(5), sqrt(-3)) or [K:Q] != 4
    # We check if the splitting field of f(x) is exactly Q(sqrt(5), sqrt(-3)).
    # This is true if and only if f(x) splits completely over Q(sqrt(5), sqrt(-3))
    # but does NOT split completely over any of its proper subfields:
    # Q, Q(sqrt(5)), Q(sqrt(-3)), and Q(sqrt(-15)).
    try:
        if not h1_ok:
            neg_q = True
        else:
            sym = list(w.free_symbols)[0] if w.free_symbols else sympy.Symbol('x')
            
            def check(ext):
                try:
                    if ext is None:
                        p_ext = Poly(w, sym, domain='QQ')
                    else:
                        p_ext = Poly(w, sym, extension=ext)
                    _, factors = p_ext.factor_list()
                    return all(fac.degree() <= 1 for fac, mult in factors)
                except Exception:
                    return False
            
            c_all = check(sqrt(5) + sqrt(-3))
            if not c_all:
                neg_q = True
            else:
                c_Q = check(None)
                c_5 = check(sqrt(5))
                c_3 = check(sqrt(-3))
                c_15 = check(sqrt(-15))
                
                conclusion_true = c_all and not c_Q and not c_5 and not c_3 and not c_15
                neg_q = not conclusion_true
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The splitting field of f(x) is not Q(sqrt(5), sqrt(-3)) or its degree is not 4"
]

N_HYP = 1
NEG_Q_INDEX = 1