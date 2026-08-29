import sympy as sp
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: Phi_n is the n-th cyclotomic polynomial",
    "not Q: Phi_n is not irreducible over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    x_sym = sp.Symbol('x')
    
    n = None
    f = None
    
    if isinstance(witness, tuple) and len(witness) == 2:
        n_raw, f_raw = witness
        try:
            n = int(n_raw)
        except Exception:
            n = n_raw
        try:
            f = sp.sympify(f_raw)
        except Exception:
            f = f_raw
    else:
        try:
            n_val = int(witness)
            if float(witness) == n_val:
                n = n_val
            else:
                f = sp.sympify(witness)
        except Exception:
            try:
                f = sp.sympify(witness)
            except Exception:
                f = witness

    if f is None and n is not None:
        try:
            if isinstance(n, int) and n >= 1:
                f = sp.cyclotomic_poly(n, x_sym)
        except Exception:
            pass

    h1_ok = False
    try:
        if n is not None and f is not None:
            if isinstance(n, int) and n >= 1:
                expected = sp.cyclotomic_poly(n, x_sym)
                if hasattr(f, 'free_symbols'):
                    f_syms = list(f.free_symbols)
                    if len(f_syms) == 1:
                        sym = f_syms[0]
                        h1_ok = sp.expand(f - expected.subs(x_sym, sym)) == 0
                    elif len(f_syms) == 0:
                        h1_ok = sp.expand(f - expected) == 0
        elif f is not None and hasattr(f, 'free_symbols'):
            f_syms = list(f.free_symbols)
            if len(f_syms) == 1:
                sym = f_syms[0]
                f_x = f.subs(sym, x_sym)
                deg = sp.degree(f_x, x_sym)
                max_n = min(10000, max(10, int(deg)**2 + 2))
                for test_n in range(1, max_n):
                    if sp.totient(test_n) == deg:
                        if sp.expand(f_x - sp.cyclotomic_poly(test_n, x_sym)) == 0:
                            h1_ok = True
                            break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if f is not None and hasattr(f, 'free_symbols'):
            factors = sp.factor_list(f, domain='QQ')
            if len(factors[1]) == 1 and factors[1][0][1] == 1:
                poly_factor = factors[1][0][0]
                f_syms = list(poly_factor.free_symbols)
                if len(f_syms) == 1:
                    sym = f_syms[0]
                    if sp.degree(poly_factor, sym) > 0:
                        neg_q_ok = False
                    else:
                        neg_q_ok = True
                else:
                    neg_q_ok = True
            else:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]