import sympy
from sympy import limit, oo, Symbol

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, positive=True)
k = Symbol('k', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "H_2: (x_{n_k}) is a subsequence of (x_n)",
    "¬Q: The subsequence (x_{n_k}) does not converge to L"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                x_obj, n_k_obj, L = witness
                check_L = True
            elif len(witness) == 2:
                x_obj, n_k_obj = witness
                check_L = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if callable(x_obj):
            x_expr = x_obj(n)
        else:
            x_expr = x_obj
            
        if callable(n_k_obj):
            n_k_expr = n_k_obj(k)
        else:
            n_k_expr = n_k_obj
            
        x_expr = sympy.sympify(x_expr)
        n_k_expr = sympy.sympify(n_k_expr)
    except Exception:
        return [False, False, False]

    # H_1: (x_n) is a sequence of real numbers
    try:
        h1 = True
        for i in range(1, 20):
            val = x_expr.subs(n, i)
            val_f = val.evalf()
            if val_f.is_real is False:
                h1 = False
                break
            if not val_f.is_number:
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: (x_{n_k}) is a subsequence of (x_n)
    try:
        h2 = True
        prev = 0
        for i in range(1, 20):
            val = n_k_expr.subs(k, i)
            try:
                if val.is_integer is False:
                    h2 = False
                    break
                if val != sympy.floor(val):
                    h2 = False
                    break
                val_int = int(val)
            except TypeError:
                h2 = False
                break
            if val_int <= prev:
                h2 = False
                break
            prev = val_int
    except Exception:
        h2 = False

    # ¬Q: The subsequence (x_{n_k}) does not converge to L
    try:
        subseq_expr = x_expr.subs(n, n_k_expr)
        lim = limit(subseq_expr, k, oo)
        
        if check_L:
            if lim == L:
                neg_q = False
            else:
                try:
                    if sympy.simplify(lim - L) == 0:
                        neg_q = False
                    else:
                        neg_q = True
                except Exception:
                    neg_q = True
        else:
            if lim.has(sympy.oo, -sympy.oo, sympy.zoo) or "AccumBounds" in str(type(lim)):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]