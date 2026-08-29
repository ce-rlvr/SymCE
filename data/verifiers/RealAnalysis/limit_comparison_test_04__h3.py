import sympy
from sympy import Symbol, Sum, oo

# Top-level setup for witness expressions
n = Symbol('n', integer=True, positive=True)
k = Symbol('k', integer=True, positive=True)

def _eval_expr(expr, i):
    """Helper to substitute all free symbols in an expression with integer i."""
    if not hasattr(expr, 'free_symbols'):
        return expr
    subs_dict = {s: i for s in expr.free_symbols}
    return expr.subs(subs_dict)

def conditions(witness) -> list[bool]:
    try:
        a_n, b_n, L = witness
    except Exception:
        return [False, False, False, False]
    
    # Handle cases where the witness provides functions instead of expressions
    try:
        if callable(a_n):
            a_expr = a_n(n)
        else:
            a_expr = a_n
            
        if callable(b_n):
            b_expr = b_n(n)
        else:
            b_expr = b_n
    except Exception:
        a_expr = a_n
        b_expr = b_n

    # H_1: sum a_n and sum b_n are infinite series of real numbers
    try:
        h1 = True
        for i in range(1, 11):
            va = complex(_eval_expr(a_expr, i))
            vb = complex(_eval_expr(b_expr, i))
            if abs(va.imag) > 1e-9 or abs(vb.imag) > 1e-9:
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: a_n > 0 and b_n > 0 for all n >= 1
    try:
        h2 = True
        for i in range(1, 101):
            va = float(_eval_expr(a_expr, i))
            vb = float(_eval_expr(b_expr, i))
            if va <= 0 or vb <= 0:
                h2 = False
                break
    except Exception:
        h2 = False

    # H_3: 0 < L < \infty
    try:
        L_val = float(L)
        h3 = (0 < L_val < float('inf'))
    except Exception:
        h3 = False

    # ¬Q: The series sum a_n converges if and only if sum b_n converges (MUST FAIL)
    # So exactly one converges and the other diverges.
    try:
        sym_a = list(a_expr.free_symbols)[0] if hasattr(a_expr, 'free_symbols') and a_expr.free_symbols else n
        sym_b = list(b_expr.free_symbols)[0] if hasattr(b_expr, 'free_symbols') and b_expr.free_symbols else n
        
        conv_a = Sum(a_expr, (sym_a, 1, oo)).is_convergent()
        conv_b = Sum(b_expr, (sym_b, 1, oo)).is_convergent()
        
        if conv_a is None or conv_b is None:
            neg_q = False
        else:
            neg_q = bool(conv_a) != bool(conv_b)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: sum a_n and sum b_n are infinite series of real numbers",
    "H_2: a_n > 0 and b_n > 0 for all n >= 1",
    "H_3: 0 < L < oo",
    "¬Q: Exactly one of sum a_n or sum b_n converges"
]

N_HYP = 3
NEG_Q_INDEX = 3