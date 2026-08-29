import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference.
n = sp.Symbol('n', integer=True, positive=True)
k = sp.Symbol('k', integer=True, positive=True)
x = sp.Symbol('x')

def conditions(witness):
    a_expr = None
    c_expr = None
    R_val = None

    # Extract witness components
    if isinstance(witness, dict):
        a_expr = witness.get('a')
        c_expr = witness.get('c')
        R_val = witness.get('R')
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 3:
            a_expr = witness[0]
            c_expr = witness[1]
            R_val = witness[2]
        elif len(witness) == 2:
            a_expr = witness[0]
            R_val = witness[1]

    if a_expr is None or R_val is None:
        return [False, False]

    if isinstance(a_expr, (list, tuple)):
        return [False, False]

    # Construct c_expr if missing
    if c_expr is None:
        try:
            if callable(a_expr):
                a_sym = a_expr(k)
            else:
                a_sym = sp.sympify(a_expr).subs(n, k)
            c_sym = sp.Sum(a_sym, (k, 1, n)).doit() / n
            c_expr = c_sym
        except Exception:
            return [False, False]

    # Check H_1: c_n = (1/n) sum_{k=1}^n a_k
    H1 = True
    try:
        for i in range(1, 20):
            sum_a = 0
            for j in range(1, i+1):
                if callable(a_expr):
                    val = a_expr(j)
                else:
                    val = sp.sympify(a_expr).subs(n, j)
                sum_a += val
            expected_c = sp.simplify(sum_a / i)

            if callable(c_expr):
                actual_c = c_expr(i)
            else:
                actual_c = sp.sympify(c_expr).subs(n, i)

            diff = sp.simplify(actual_c - expected_c)
            if diff != 0:
                diff = sp.cancel(sp.expand(diff))
                if diff != 0:
                    H1 = False
                    break
    except Exception:
        H1 = False

    # Check neg_Q: R_c < min(R, 1)
    neg_Q = False
    try:
        if callable(c_expr):
            c_sym = c_expr(n)
        else:
            c_sym = sp.sympify(c_expr)

        Rc_val = None

        if c_sym.has(sp.Sum):
            pass  # Cannot reliably compute limit of unsimplified sum
        elif sp.simplify(c_sym) == 0:
            Rc_val = float('inf')
        else:
            # Try ratio test
            try:
                ratio = sp.simplify(c_sym / c_sym.subs(n, n+1))
                L = sp.limit(sp.Abs(ratio), n, sp.oo)
                if L == sp.oo:
                    Rc_val = float('inf')
                elif L.is_number:
                    Rc_val = float(L)
            except Exception:
                pass

            # Try root test if ratio test fails
            if Rc_val is None:
                try:
                    root = sp.Abs(c_sym)**(1/n)
                    L = sp.limit(root, n, sp.oo)
                    if L == 0:
                        Rc_val = float('inf')
                    elif L == sp.oo:
                        Rc_val = 0.0
                    elif L.is_number:
                        Rc_val = float(1/L)
                except Exception:
                    pass

        if Rc_val is not None:
            if R_val == sp.oo or str(R_val) == 'oo' or R_val == float('inf'):
                R_num = float('inf')
            else:
                R_num = float(R_val)
            neg_Q = Rc_val < min(R_num, 1.0)
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: c_n = (1/n) sum_{k=1}^n a_k for all integers n >= 1",
    "¬Q: The radius of convergence of sum c_n x^n is < min(R, 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1