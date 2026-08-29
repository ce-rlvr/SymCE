import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, n = sp.symbols('x n', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (K, F) where K is a tuple (a, b) representing the 
    interval [a, b], and F is a sympy expression in terms of x and n representing 
    the family of functions F_n(x).
    """
    # H1: K is a compact metric space
    try:
        K, F = witness
        a, b = K
        a = float(a)
        b = float(b)
        h1 = (a <= b)
    except Exception:
        h1 = False

    # H2: F is a family of continuous real-valued functions on K
    try:
        h2 = True
        for nv in [1, 2, 3]:
            F_n = F.subs(n, nv)
            
            # Check for obvious singularities in the interval
            try:
                sings = sp.singularities(F_n, x)
                for s in sings:
                    if s.is_real and min(a, b) <= s <= max(a, b):
                        h2 = False
                        break
            except Exception:
                pass
            
            if not h2:
                break
                
            # Grid check to ensure it evaluates to finite real numbers
            F_n_func = sp.lambdify(x, F_n, modules=['math', 'sympy'])
            step = (b - a) / 100 if b != a else 0
            for i in range(101):
                xv = a + i * step
                try:
                    val = float(F_n_func(xv))
                    if math.isnan(val) or math.isinf(val):
                        h2 = False
                        break
                except Exception:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H3: F is pointwise bounded on K
    try:
        h3 = True
        step = (b - a) / 10 if b != a else 0
        for i in range(11):
            xv = a + i * step
            F_x = F.subs(x, xv)
            if F_x.is_constant():
                continue
            
            try:
                L = sp.limit(F_x, n, sp.oo)
                if isinstance(L, sp.Limit):
                    raise ValueError("Limit unevaluated")
                if L.has(sp.oo, -sp.oo, sp.zoo):
                    h3 = False
                    break
            except Exception:
                # Fallback: check values for increasing n
                F_x_func = sp.lambdify(n, F_x, modules=['math', 'sympy'])
                vals = []
                for nv in [10, 100, 1000, 10000]:
                    try:
                        vals.append(float(abs(F_x_func(nv))))
                    except Exception:
                        pass
                if len(vals) >= 2 and vals[-1] > vals[0] * 2 and vals[-1] > 100:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: F is not uniformly bounded on K
    try:
        max_vals = []
        # Evaluate the maximum of |F_n(x)| on K for increasing n
        for nv in [10, 100, 1000, 10000]:
            F_n = F.subs(n, nv)
            F_n_func = sp.lambdify(x, F_n, modules=['math', 'sympy'])
            step = (b - a) / 1000 if b != a else 0
            mval = -1.0
            for i in range(1001):
                xv = a + i * step
                try:
                    val = float(abs(F_n_func(xv)))
                    if val > mval:
                        mval = val
                except Exception:
                    pass
            if mval >= 0:
                max_vals.append(mval)
        
        neg_q = False
        if len(max_vals) == 4:
            diff1 = max_vals[1] - max_vals[0]
            diff2 = max_vals[2] - max_vals[1]
            diff3 = max_vals[3] - max_vals[2]
            
            # For an unbounded family, the maximums should grow indefinitely.
            # We check that the growth is not just asymptotically approaching a bound.
            if diff3 > 0.5 * diff2 and diff3 > 0.5:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a compact metric space",
    "H_2: F is a family of continuous real-valued functions on K",
    "H_3: F is pointwise bounded on K",
    "¬Q: F is not uniformly bounded on K"
]

N_HYP = 3
NEG_Q_INDEX = 3