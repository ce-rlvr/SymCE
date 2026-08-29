import sympy
from sympy import S
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sympy.symbols('x y z', real=True)

CONDITION_LABELS = [
    "H_1: f is strictly convex",
    "H_2: f is continuously differentiable",
    "¬Q: The Legendre-Fenchel transform f* is not continuously differentiable everywhere with gradient (nabla f)^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Determine the variable used in the witness expression
    if hasattr(witness, "free_symbols"):
        syms = list(witness.free_symbols)
        if x in syms:
            sym = x
        elif syms:
            sym = syms[0]
        else:
            sym = x
    else:
        try:
            witness = sympy.sympify(witness)
            syms = list(witness.free_symbols)
            if x in syms:
                sym = x
            elif syms:
                sym = syms[0]
            else:
                sym = x
        except Exception:
            return [False, False, False]

    # H1: f is strictly convex
    try:
        f_prime = witness.diff(sym)
        f_double_prime = f_prime.diff(sym)
        
        # Evaluate the second derivative at a grid of points to check strict convexity
        pts = [i/10.0 for i in range(-100, 101)]
        h1_ok = True
        zeros = 0
        for p in pts:
            try:
                val = float(f_double_prime.subs(sym, p).evalf())
            except Exception:
                h1_ok = False
                break
            if val < -1e-7:
                h1_ok = False
                break
            if abs(val) <= 1e-7:
                zeros += 1
        # If the second derivative is zero on a large interval, it is not strictly convex
        if zeros > 20:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H2: f is continuously differentiable
    try:
        from sympy.calculus.util import continuous_domain
        dom_f = continuous_domain(witness, sym, S.Reals)
        dom_df = continuous_domain(f_prime, sym, S.Reals)
        h2_ok = (dom_f == S.Reals) and (dom_df == S.Reals)
    except Exception:
        # Fallback if continuous_domain fails
        try:
            h2_ok = True
            for p in pts:
                try:
                    v1 = float(witness.subs(sym, p).evalf())
                    v2 = float(f_prime.subs(sym, p).evalf())
                except Exception:
                    h2_ok = False
                    break
        except Exception:
            h2_ok = False

    # neg_Q: f* is not continuously differentiable everywhere with gradient (f')^{-1}
    # This happens if and only if the range of f' is not the entirety of R.
    # Since f' is strictly increasing (by H1), we just check its limits at +/- infinity.
    try:
        limit_inf = sympy.limit(f_prime, sym, sympy.oo)
        if hasattr(limit_inf, 'has') and limit_inf.has(sympy.Limit):
            # Fallback for unevaluated limits
            val_inf = float(f_prime.subs(sym, 1e6).evalf())
            inf_ok = (val_inf < 1e5)
        else:
            inf_ok = (limit_inf != sympy.oo)
    except Exception:
        inf_ok = False

    try:
        limit_minf = sympy.limit(f_prime, sym, -sympy.oo)
        if hasattr(limit_minf, 'has') and limit_minf.has(sympy.Limit):
            # Fallback for unevaluated limits
            val_minf = float(f_prime.subs(sym, -1e6).evalf())
            minf_ok = (val_minf > -1e5)
        else:
            minf_ok = (limit_minf != -sympy.oo)
    except Exception:
        minf_ok = False

    try:
        neg_q_ok = inf_ok or minf_ok
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]