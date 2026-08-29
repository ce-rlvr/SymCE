import sympy
from sympy import Symbol, S
from sympy.calculus.util import continuous_domain
import math

# Top-level setup
x = Symbol('x', real=True)

def num_int(f_expr, a_val, b_val, use_abs=False):
    """Numerical integration using composite Simpson's 1/3 rule."""
    try:
        f_lam = sympy.lambdify(x, f_expr, 'math')
        f_lam(a_val)  # test evaluation
        N = 1000
        dt = (b_val - a_val) / N
        total = 0
        for i in range(N + 1):
            v = f_lam(a_val + i * dt)
            if use_abs:
                v = abs(v)
            if i == 0 or i == N:
                total += v
            elif i % 2 == 1:
                total += 4 * v
            else:
                total += 2 * v
        return total * dt / 3
    except Exception:
        # Fallback to sympy subs and evalf if lambdify fails
        N = 200
        dt = (b_val - a_val) / N
        total = 0
        for i in range(N + 1):
            v = float(f_expr.subs(x, a_val + i * dt).evalf())
            if use_abs:
                v = abs(v)
            if i == 0 or i == N:
                total += v
            elif i % 2 == 1:
                total += 4 * v
            else:
                total += 2 * v
        return total * dt / 3

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the conjecture.
    witness should be a tuple (f, T, a, b) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            T = witness.get('T')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, T, a, b = witness
    except Exception:
        return [False, False, False, False]

    # H1: f is a continuous, real-valued function on R
    try:
        dom = continuous_domain(f, x, S.Reals)
        h1 = (dom == S.Reals)
    except Exception:
        h1 = False

    # H2: T > 0 and f(x+T) = f(x) for all x
    try:
        T_val = float(T)
        if T_val <= 0:
            h2 = False
        else:
            diff = sympy.simplify(f.subs(x, x + T) - f)
            if diff == 0:
                h2 = True
            else:
                # Fallback to numerical check
                h2 = True
                for val in [0.1, 0.5, 1.2, 3.14159]:
                    v1 = float(f.subs(x, val).evalf())
                    v2 = float(f.subs(x, val + T_val).evalf())
                    if abs(v1 - v2) > 1e-5:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H3: integral of f from 0 to T is 0
    try:
        int_val = sympy.integrate(f, (x, 0, T))
        if sympy.simplify(int_val) == 0:
            h3 = True
        else:
            # Fallback to numerical check
            val = num_int(f, 0, float(T), use_abs=False)
            h3 = abs(val) < 1e-5
    except Exception:
        try:
            val = num_int(f, 0, float(T), use_abs=False)
            h3 = abs(val) < 1e-5
        except Exception:
            h3 = False

    # Negated Conclusion: |int_a^b f(x) dx| > 1/2 int_0^T |f(x)| dx
    try:
        a_val = float(a)
        b_val = float(b)
        T_val = float(T)
        
        lhs_val = abs(num_int(f, a_val, b_val, use_abs=False))
        rhs_val = 0.5 * num_int(f, 0, T_val, use_abs=True)
        
        # We use a small tolerance to avoid false positives due to floating point inaccuracies
        neg_q = bool(lhs_val > rhs_val + 1e-5)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuous, real-valued function on R",
    "H_2: T is a strictly positive real number such that f(x+T) = f(x)",
    "H_3: integral of f from 0 to T is 0",
    "¬Q: |int_a^b f(x) dx| > 1/2 int_0^T |f(x)| dx"
]

N_HYP = 3
NEG_Q_INDEX = 3