import sympy as sp

n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    # Parse witness: can be a single expression/function or a tuple (a, p)
    if isinstance(witness, tuple) and len(witness) == 2:
        a_obj, p_obj = witness
    else:
        a_obj = witness
        p_obj = witness

    # Evaluate if callable to get symbolic expressions in terms of n
    if callable(a_obj):
        try:
            a_expr = a_obj(n)
        except Exception:
            a_expr = a_obj
    else:
        a_expr = a_obj

    if callable(p_obj):
        try:
            p_expr = p_obj(n)
        except Exception:
            p_expr = p_obj
    else:
        p_expr = p_obj

    # Convert to sympy objects
    try:
        a_expr = sp.sympify(a_expr)
        p_expr = sp.sympify(p_expr)
    except Exception:
        pass

    # H_1: a_n = p(n) for all integers n >= 1
    h1_ok = False
    try:
        if a_expr == p_expr:
            h1_ok = True
        else:
            diff = sp.simplify(a_expr - p_expr)
            if diff == 0:
                h1_ok = True
            else:
                h1_ok = all(sp.simplify(a_expr.subs(n, i) - p_expr.subs(n, i)) == 0 for i in range(1, 10))
    except Exception:
        h1_ok = False

    # neg_Q: The radius of convergence of the power series sum a_n x^n is NOT exactly 1
    neg_q_ok = False
    try:
        if a_expr == 0:
            neg_q_ok = True
        else:
            # Try ratio test: R = lim |a_n / a_{n+1}|
            ratio = sp.Abs(a_expr / a_expr.subs(n, n + 1))
            L = sp.limit(ratio, n, sp.oo)
            if L == 1:
                neg_q_ok = False
            elif L == sp.nan:
                raise ValueError("Ratio limit is nan")
            elif L.is_number or L == sp.oo:
                neg_q_ok = True
            else:
                raise ValueError("Ratio limit not a number")
    except Exception:
        try:
            # Try root test: R = 1 / lim |a_n|^(1/n)
            root = sp.limit(sp.Abs(a_expr)**(1/n), n, sp.oo)
            if root == 1:
                neg_q_ok = False
            elif root == sp.nan:
                raise ValueError("Root limit is nan")
            elif root.is_number or root == sp.oo:
                neg_q_ok = True
            else:
                neg_q_ok = False
        except Exception:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a_n = p(n) for all integers n >= 1",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1