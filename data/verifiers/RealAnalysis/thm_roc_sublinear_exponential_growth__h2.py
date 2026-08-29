import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup
n = Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a sympy expression in terms of n, or a callable.
    """
    # H1: (a_n) is a sequence of non-zero real numbers.
    h1 = False
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
            
        is_valid = True
        for i in range(20):
            val = expr.subs(n, i)
            if val == 0 or sympy.simplify(val) == 0:
                is_valid = False
                break
            if val.is_real is False:
                is_valid = False
                break
            try:
                cval = complex(val.evalf())
                if abs(cval.imag) > 1e-12:
                    is_valid = False
                    break
            except Exception:
                pass
        h1 = is_valid
    except Exception:
        h1 = False

    # neg_Q: The radius of convergence of the power series is NOT exactly 1.
    neg_q = False
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
            
        expr_next = expr.subs(n, n + 1)
        ratio = Abs(expr / expr_next)
        R = limit(ratio, n, oo)
        
        if R == 1:
            neg_q = False
        elif R.is_number or R == oo:
            neg_q = True
        else:
            # Fallback to root test if ratio test limit is unevaluated
            root = Abs(expr)**(1/n)
            L = limit(root, n, oo)
            if L == 1:
                neg_q = False
            elif L.is_number or L == oo:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of non-zero real numbers",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1