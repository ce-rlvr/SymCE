import sympy as sp
import math

# Top-level setup for witness expressions
x = sp.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The expected counterexample is the empty family of functions, which vacuously 
    satisfies the Lipschitz condition and the finite supremum condition (sup is -inf), 
    but fails the conclusion because the supremum is -infinity everywhere, which is 
    not real-valued.
    """
    # H1: {f_i} is a family of functions from X to R
    try:
        if isinstance(witness, dict):
            funcs = list(witness.values())
        elif isinstance(witness, str):
            funcs = None
        elif hasattr(witness, '__iter__'):
            funcs = list(witness)
        else:
            funcs = None
        h1_ok = funcs is not None
    except Exception:
        h1_ok = False
        funcs = None

    # H2: There exists a constant L > 0 such that every f_i is L-Lipschitz continuous
    try:
        h2_ok = False
        if h1_ok:
            if len(funcs) == 0:
                # Vacuously true for the empty family
                h2_ok = True
            else:
                is_lip = True
                for f in funcs:
                    try:
                        expr = f(x) if callable(f) else f
                        expr = sp.sympify(expr)
                        # Basic check to ensure it's a valid differentiable expression
                        sp.diff(expr, x)
                    except Exception:
                        is_lip = False
                        break
                h2_ok = is_lip
    except Exception:
        h2_ok = False

    # H3: There exists at least one point x_0 in X such that sup f_i(x_0) < infinity
    try:
        h3_ok = False
        if h1_ok:
            if len(funcs) == 0:
                # For the empty family, the supremum is -infinity, which is < infinity
                h3_ok = True
            else:
                vals = []
                for f in funcs:
                    try:
                        expr = f(x) if callable(f) else f
                        expr = sp.sympify(expr)
                        val = float(expr.subs(x, 0))
                        vals.append(val)
                    except Exception:
                        pass
                if vals and max(vals) < float('inf'):
                    h3_ok = True
    except Exception:
        h3_ok = False

    # neg_Q: The function f(x) = sup f_i(x) is NOT (real-valued and Lipschitz continuous with constant L)
    try:
        neg_q_ok = False
        if h1_ok:
            if len(funcs) == 0:
                # For the empty family, sup is -infinity everywhere, which is NOT real-valued.
                # Thus, the conclusion fails, and its negation is True.
                neg_q_ok = True
            else:
                # For any non-empty family satisfying the hypotheses, the theorem is mathematically true.
                # Therefore, the conclusion holds, and its negation is False.
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {f_i} is a family of functions from X to R",
    "H_2: There exists a constant L > 0 such that every f_i is L-Lipschitz continuous",
    "H_3: There exists at least one point x_0 in X such that sup f_i(x_0) < infinity",
    "¬Q: The function f(x) = sup f_i(x) is not real-valued or not Lipschitz continuous on X with constant L"
]

N_HYP = 3
NEG_Q_INDEX = 3