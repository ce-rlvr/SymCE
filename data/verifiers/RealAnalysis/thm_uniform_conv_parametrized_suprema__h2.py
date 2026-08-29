import math
import sympy
from sympy import Symbol, Rational

# Top-level setup for potential symbolic expressions
x, y, n = sympy.symbols('x y n', real=True)

CONDITION_LABELS = [
    "H_1: (f_n(x, y)) is a sequence of real-valued functions defined on X x Y",
    "H_2: For each n and each x in X, the supremum g_n(x) = sup_{y in Y} f_n(x, y) is finite",
    "¬Q: The sequence g_n(x) does not converge uniformly to g(x) = sup_{y in Y} f(x, y) on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def extract_points(S):
    """Helper to extract a finite list of test points from a domain representation."""
    if hasattr(S, 'is_Interval') and S.is_Interval:
        try:
            return [float(S.start), float(S.end), float((S.start + S.end)/2)]
        except Exception:
            return [0.0, 1.0]
    if hasattr(S, 'is_FiniteSet') and S.is_FiniteSet:
        return list(S)
    try:
        iter(S)
        if isinstance(S, (str, dict)):
            return [S]
        return list(S)
    except TypeError:
        return [S]

def conditions(witness):
    if isinstance(witness, dict):
        X_raw = witness.get("X", [0.0, 1.0])
        Y_raw = witness.get("Y", [0.0, 1.0])
        f_n = witness.get("f_n")
        f = witness.get("f")
    else:
        X_raw = getattr(witness, "X", [0.0, 1.0])
        Y_raw = getattr(witness, "Y", [0.0, 1.0])
        f_n = getattr(witness, "f_n", None)
        f = getattr(witness, "f", None)
        
    if f_n is None or f is None:
        return [False, False, False]

    X = extract_points(X_raw)
    Y = extract_points(Y_raw)

    if not X or not Y:
        return [False, False, False]

    # H1: f_n is a sequence of real-valued functions on X x Y
    h1 = True
    try:
        for n_val in [1, 2, 3]:
            for x_val in X:
                for y_val in Y:
                    val = f_n(n_val, x_val, y_val)
                    if not isinstance(val, (int, float)):
                        if hasattr(val, 'is_real') and val.is_real:
                            pass
                        else:
                            h1 = False
    except Exception:
        h1 = False

    # H2: g_n(x) is finite
    h2 = True
    try:
        for n_val in [1, 2, 3]:
            for x_val in X:
                vals = [float(f_n(n_val, x_val, y_val)) for y_val in Y]
                gn = max(vals)
                if math.isinf(gn) or math.isnan(gn):
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: g_n(x) does not converge uniformly to g(x)
    neg_q = False
    try:
        converges_to_g = True
        for x_val in X:
            gx = max([float(f(x_val, y_val)) for y_val in Y])
            
            # Evaluate at large n to check for convergence to g(x)
            # We check both an even and an odd large n to catch oscillating sequences
            gn_even = max([float(f_n(10000, x_val, y_val)) for y_val in Y])
            gn_odd  = max([float(f_n(10001, x_val, y_val)) for y_val in Y])
            
            # If the sequence is still far from g(x) at large n, it does not converge to g(x)
            if abs(gn_even - gx) > 1e-2 or abs(gn_odd - gx) > 1e-2:
                converges_to_g = False
                break
                
        neg_q = not converges_to_g
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]