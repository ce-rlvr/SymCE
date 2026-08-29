import sympy as sp
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
x, w = sp.symbols('x w')

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with:
      - 'X': a tuple (a, b) representing the bounded open interval.
      - 'Omega': a list of points representing a finite discrete sample space.
      - 'P': a list of probabilities for each point in Omega.
      - 'f': a sympy expression in terms of `x` and `w` representing f(x, w).
    """
    # H_1: X is an open interval in R
    try:
        a, b = sp.sympify(witness['X'][0]), sp.sympify(witness['X'][1])
        h1 = a.is_real and b.is_real and (a < b) and a.is_finite and b.is_finite
    except Exception:
        h1 = False

    # H_2: (Omega, A, P) is a probability space
    try:
        Omega = witness['Omega']
        P = witness['P']
        h2 = len(Omega) == len(P) and len(Omega) > 0
        sum_P = 0
        for p in P:
            p_val = sp.sympify(p)
            if not (p_val >= 0):
                h2 = False
            sum_P += p_val
        # Check if probabilities sum to 1
        if abs(float(sum_P) - 1.0) > 1e-9:
            h2 = False
    except Exception:
        h2 = False

    # H_3: f(., w) is differentiable on X for almost all w
    try:
        f_expr = sp.sympify(witness['f'])
        h3 = True
        midpoint = (a + b) / 2
        for omega, p in zip(Omega, P):
            if sp.sympify(p) > 0:
                f_w = f_expr.subs(w, omega)
                
                # Check if f_w is real-valued on the interval (using midpoint as a proxy)
                try:
                    val = complex(f_w.subs(x, midpoint).evalf())
                    if abs(val.imag) > 1e-9:
                        h3 = False
                        break
                except Exception:
                    h3 = False
                    break

                df_w = sp.diff(f_w, x)
                
                # Check for singularities in the open interval (a, b)
                sings = sp.singularities(f_w, x, sp.Interval.open(a, b))
                sings_df = sp.singularities(df_w, x, sp.Interval.open(a, b))
                
                if sings.is_empty != True or sings_df.is_empty != True:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: The family F is NOT uniformly equicontinuous on X
    # For a finite family, uniform equicontinuity is equivalent to every function being uniformly continuous.
    # On a bounded open interval, uniform continuity implies finite limits at the endpoints.
    try:
        neg_Q = False
        for r in range(len(Omega) + 1):
            for subset_indices in itertools.combinations(range(len(Omega)), r):
                g_A = 0
                for idx in subset_indices:
                    g_A += f_expr.subs(w, Omega[idx]) * sp.sympify(P[idx])
                
                L_a = sp.limit(g_A, x, a, dir='+')
                L_b = sp.limit(g_A, x, b, dir='-')
                
                def is_finite_limit(L):
                    if isinstance(L, sp.Limit):
                        return True  # Assume finite to avoid false positive neg_Q on unevaluated limits
                    if L.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                        return False
                    if type(L).__name__ == 'AccumBounds':
                        return False
                    if L.is_finite is False:
                        return False
                    return True
                
                # If any function in the family lacks finite limits at the endpoints, it's not uniformly continuous
                if not is_finite_limit(L_a) or not is_finite_limit(L_b):
                    neg_Q = True
                    break
            if neg_Q:
                break
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: X is an open interval in R",
    "H_2: (Omega, A, P) is a probability space",
    "H_3: f(., w) is differentiable on X for almost all w",
    "¬Q: The family F is not uniformly equicontinuous on X"
]

N_HYP = 3
NEG_Q_INDEX = 3