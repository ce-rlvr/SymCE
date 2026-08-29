import sympy as sp
from sympy.abc import x, y, z
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness.get('a', 0)
            b = witness.get('b', 1)
            L = witness.get('L', 1)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                f, a, b, L = witness
            elif len(witness) == 3:
                f, a, b = witness
                L = 1
            elif len(witness) == 2:
                f, L = witness
                a, b = 0, 1
            else:
                f = witness[0]
                a, b, L = 0, 1, 1
        else:
            f = witness
            a, b, L = 0, 1, 1
            
        if not isinstance(f, sp.Expr):
            f = sp.sympify(f)
            
        a_f = float(a)
        b_f = float(b)
        L_f = float(L)
        
        h1 = (a_f < b_f) and (L_f >= 0)
    except Exception:
        h1 = False

    try:
        free_syms = f.free_symbols
        if len(free_syms) >= 1:
            if x in free_syms:
                var = x
            else:
                var = list(free_syms)[0]
        else:
            var = x

        df = sp.diff(f, var)
        neg_q = False
        n_samples = 500
        
        f_vals = []
        for i in range(n_samples + 1):
            t = a_f + (b_f - a_f) * i / n_samples
            
            try:
                val = float(abs(df.subs(var, t)))
                if val > L_f + 1e-5:
                    neg_q = True
                    break
            except Exception:
                pass
            
            try:
                f_vals.append((t, float(f.subs(var, t))))
            except Exception:
                pass
                
        if not neg_q:
            for i in range(len(f_vals)):
                for j in range(i + 1, min(i + 20, len(f_vals))):
                    t1, y1 = f_vals[i]
                    t2, y2 = f_vals[j]
                    if t2 > t1:
                        if abs(y2 - y1) > L_f * (t2 - t1) + 1e-5:
                            neg_q = True
                            break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V(x) denotes the total variation of f on the interval a to x",
    "¬Q: V(x) is not L-Lipschitz continuous"
]

N_HYP = 1
NEG_Q_INDEX = 1