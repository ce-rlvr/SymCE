import sympy
from sympy import Symbol

x = Symbol('x', real=True)
n = Symbol('n', integer=True)

def get_P_i(P, i, n_sym):
    if isinstance(P, (list, tuple)):
        idx = i - 1 if (i - 1) < len(P) else -1
        return P[idx]
    elif callable(P):
        return P(i)
    else:
        return P.subs(n_sym, i)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            P, f = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H1: P_n is a sequence of polynomial functions
    h1_ok = False
    try:
        h1_ok = True
        for i in range(1, 101):
            P_i = get_P_i(P, i, n)
            if not sympy.sympify(P_i).is_polynomial(x):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # neg_Q: f is not a polynomial OR for all N, exists i >= N such that P_i - f is not constant
    neg_q_ok = False
    try:
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
        f_expr = sympy.sympify(f_expr)
        
        if not f_expr.is_polynomial(x):
            neg_q_ok = True
        else:
            exists_N = False
            for N_val in range(1, 101):
                all_constant = True
                for i in range(N_val, 101):
                    P_i = get_P_i(P, i, n)
                    diff_expr = sympy.sympify(P_i) - f_expr
                    deriv = sympy.diff(diff_expr, x)
                    if sympy.simplify(sympy.expand(deriv)) != 0:
                        all_constant = False
                        break
                if all_constant:
                    exists_N = True
                    break
            neg_q_ok = not exists_N
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {P_n} is a sequence of polynomial functions from R to R",
    "¬Q: f is not a polynomial function, or for all N there is n >= N such that P_n(x) - f(x) is not constant"
]

N_HYP = 1
NEG_Q_INDEX = 1