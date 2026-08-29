import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup
n = Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    """
    # 1. Evaluate the witness to a sympy expression
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
    except Exception:
        return [False, False, False]

    # 2. Check if the sequence is eventually zero (for neg_Q)
    try:
        is_eventually_zero = True
        # Check a few large indices to see if it becomes zero
        for k in [100, 500, 1000, 5000]:
            val = sympy.N(expr.subs(n, k), 50)
            if val != 0:
                is_eventually_zero = False
                break
        # The conclusion is "eventually zero". We want the NEGATION of the conclusion.
        neg_q = not is_eventually_zero
    except Exception:
        neg_q = False

    # 3. Determine the radius of convergence R (for H1 and H2)
    h1 = False
    R = None

    if is_eventually_zero:
        # If it's eventually zero, it's a polynomial, so R = infinity
        R = oo
        h1 = True
    else:
        # Try Ratio Test
        try:
            ratio = sympy.simplify(expr.subs(n, n+1) / expr)
            L = limit(Abs(ratio), n, oo)
            if isinstance(L, sympy.Limit) or "Limit" in str(L) or "AccumBounds" in str(L):
                raise ValueError("Unevaluated limit")
            if L == 0:
                R = oo
            elif L == oo:
                R = 0
            else:
                R = 1 / L
            h1 = True
        except Exception:
            # Try Root Test
            try:
                L = limit(Abs(expr)**(1/n), n, oo)
                if isinstance(L, sympy.Limit) or "Limit" in str(L) or "AccumBounds" in str(L):
                    raise ValueError("Unevaluated limit")
                if L == 0:
                    R = oo
                elif L == oo:
                    R = 0
                else:
                    R = 1 / L
                h1 = True
            except Exception:
                # Fallback: Numerical estimation of the limit of the ratio
                try:
                    vals = []
                    for k in [50, 100, 150, 200]:
                        v_k = sympy.N(expr.subs(n, k), 50)
                        v_k1 = sympy.N(expr.subs(n, k+1), 50)
                        if v_k != 0:
                            ratio_val = float(sympy.Abs(v_k1 / v_k))
                            vals.append(ratio_val)
                    # If the sequence of ratios is stabilizing, we estimate L
                    if len(vals) >= 2 and abs(vals[-1] - vals[-2]) < 1e-2:
                        L = vals[-1]
                        if L < 1e-7:
                            R = oo
                        else:
                            R = 1 / L
                        h1 = True
                except Exception:
                    h1 = False

    # 4. Check if R > 1 (for H2)
    try:
        if h1 and R is not None:
            if R == oo:
                h2 = True
            else:
                h2 = bool(R > 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: sum a_n x^n is a power series with radius of convergence R",
    "H_2: R > 1",
    "not Q: a_n is not eventually zero"
]

N_HYP = 2
NEG_Q_INDEX = 2