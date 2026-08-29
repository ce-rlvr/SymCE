import sympy
import math

n, x = sympy.symbols('n x')

def conditions(witness):
    try:
        if hasattr(witness, 'a'):
            a = witness.a
            k = witness.k
            R = witness.R
        elif isinstance(witness, dict):
            a = witness['a']
            k = witness['k']
            R = witness['R']
        else:
            a, k, R = witness
    except Exception:
        return [False, False]

    # H_1: k >= 1 is a positive integer
    try:
        h1_ok = isinstance(k, int) and k >= 1
    except Exception:
        h1_ok = False

    # neg_Q: The shifted series does NOT have radius of convergence R
    try:
        if isinstance(a, (list, tuple)):
            R_true = sympy.oo
        elif isinstance(a, sympy.Expr):
            symbols = a.free_symbols
            if not symbols:
                if a == 0:
                    R_true = sympy.oo
                else:
                    R_true = sympy.S(1)
            else:
                sym_n = list(symbols)[0]
                a_n = a.subs(sym_n, sym_n + k)
                a_n_plus_1 = a.subs(sym_n, sym_n + k + 1)
                ratio = sympy.Abs(a_n / a_n_plus_1)
                try:
                    R_true = sympy.limit(ratio, sym_n, sympy.oo)
                except Exception:
                    v1 = float(sympy.Abs(a.subs(sym_n, 100)))
                    v2 = float(sympy.Abs(a.subs(sym_n, 101)))
                    if v2 == 0:
                        R_true = sympy.oo
                    else:
                        R_true = v1 / v2
        elif isinstance(a, str):
            a_expr = sympy.sympify(a)
            symbols = a_expr.free_symbols
            if not symbols:
                if a_expr == 0:
                    R_true = sympy.oo
                else:
                    R_true = sympy.S(1)
            else:
                sym_n = list(symbols)[0]
                a_n = a_expr.subs(sym_n, sym_n + k)
                a_n_plus_1 = a_expr.subs(sym_n, sym_n + k + 1)
                ratio = sympy.Abs(a_n / a_n_plus_1)
                try:
                    R_true = sympy.limit(ratio, sym_n, sympy.oo)
                except Exception:
                    v1 = float(sympy.Abs(a_expr.subs(sym_n, 100)))
                    v2 = float(sympy.Abs(a_expr.subs(sym_n, 101)))
                    if v2 == 0:
                        R_true = sympy.oo
                    else:
                        R_true = v1 / v2
        elif callable(a):
            v1 = float(abs(a(100)))
            v2 = float(abs(a(101)))
            if v2 == 0:
                R_true = sympy.oo
            else:
                R_true = v1 / v2
        else:
            R_true = None
        
        if R_true is None:
            neg_q_ok = False
        else:
            if isinstance(R, str):
                if R.lower() in ['oo', 'inf', 'infinity']:
                    R_val = sympy.oo
                else:
                    R_val = float(R)
            else:
                R_val = R

            if R_true == sympy.oo and (R_val == sympy.oo or R_val == float('inf')):
                neg_q_ok = False
            elif R_true == sympy.oo:
                neg_q_ok = True
            elif R_val == sympy.oo or R_val == float('inf'):
                neg_q_ok = True
            else:
                try:
                    diff = abs(float(R_true) - float(R_val))
                    if math.isnan(diff):
                        neg_q_ok = True
                    else:
                        neg_q_ok = diff > 1e-5
                except Exception:
                    neg_q_ok = bool(R_true != R_val)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k >= 1 is a positive integer",
    "¬Q: The shifted power series does NOT have radius of convergence R"
]

N_HYP = 1
NEG_Q_INDEX = 1