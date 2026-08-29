import sympy
from sympy import Symbol, Abs, limit, oo

# Top-level setup
n = Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    Hypotheses:
      1. (a_n) is a sequence of real numbers.
      2. c_1 r^n <= |a_n| <= c_2 r^n for all integers n >= 0.
    Conclusion:
      The radius of convergence of the power series sum(a_n x^n) is exactly 1/r.
      
    Witness format: (a_expr, c1, c2, r)
    where a_expr is a sympy-compatible expression in terms of n.
    """
    try:
        a_expr, c1, c2, r = witness
    except Exception:
        return [False, False, False]

    # H1: (a_n) is a sequence of real numbers
    try:
        h1 = True
        a_sym = sympy.sympify(a_expr)
        for i in range(50):
            val = complex(a_sym.subs(n, i))
            if val.imag != 0:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: c_1 r^n <= |a_n| <= c_2 r^n for all n >= 0
    try:
        h2 = True
        for i in range(50):
            val = complex(a_sym.subs(n, i)).real
            lower = float(c1 * r**i)
            upper = float(c2 * r**i)
            # Use a small tolerance for floating point comparisons
            if not (lower - 1e-9 <= abs(val) <= upper + 1e-9):
                h2 = False
                break
    except Exception:
        h2 = False

    # Negated Conclusion: The radius of convergence is NOT exactly 1/r
    try:
        a_simp = sympy.simplify(a_sym)
        if a_simp == 0:
            R = oo
        else:
            R = sympy.nan
            # Try ratio test
            try:
                ratio = sympy.simplify(Abs(a_simp.subs(n, n) / a_simp.subs(n, n+1)))
                R = limit(ratio, n, oo)
            except Exception:
                pass
                
            if R == sympy.nan or not R.is_number:
                # Fallback to root test
                try:
                    root = Abs(a_simp)**(1/n)
                    inv_R = limit(root, n, oo)
                    if inv_R == 0:
                        R = oo
                    else:
                        R = 1 / inv_R
                except Exception:
                    pass

            if R == sympy.nan or not R.is_number:
                # Numerical estimation of limsup |a_n|^(1/n)
                vals = []
                for i in range(80, 100):
                    try:
                        v = float(Abs(a_simp.subs(n, i)))
                        if v > 0:
                            vals.append(v**(1/i))
                        elif v == 0:
                            vals.append(0.0)
                    except Exception:
                        pass
                if vals:
                    inv_R_est = max(vals)
                    if inv_R_est < 1e-7:
                        R = oo
                    else:
                        R = 1 / inv_R_est

        expected_R = 1 / sympy.sympify(r)
        if R == oo and expected_R == oo:
            neg_q = False
        elif R == oo or expected_R == oo:
            neg_q = True
        else:
            neg_q = abs(float(R) - float(expected_R)) > 1e-3
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of real numbers",
    "H_2: c_1 r^n <= |a_n| <= c_2 r^n for all n >= 0",
    "¬Q: The radius of convergence is not exactly 1/r"
]

N_HYP = 2
NEG_Q_INDEX = 2