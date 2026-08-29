import math
import sympy
from sympy.abc import x

# Top-level setup
# No specific named objects required for this real analysis conjecture.

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the conjecture.
    The witness should be a dictionary providing:
      - 'a': a function a(k, n) returning the n-th coefficient of the k-th power series in F.
      - 'M': the uniform bound for the coefficients.
      - 'K': a tuple (lower, upper) representing the interval K.
      - 'x': a function x(m) returning a sequence of points in K.
      - 'y': a function y(m) returning a sequence of points in K.
      - 'k': a function k(m) returning a sequence of indices for the family F.
      - 'epsilon': a positive constant demonstrating the failure of uniform equicontinuity.
    """
    try:
        a = witness["a"]
        M = witness["M"]
        K = witness["K"]
        x_seq = witness["x"]
        y_seq = witness["y"]
        k_seq = witness["k"]
        epsilon = witness["epsilon"]
    except Exception:
        return [False, False, False]

    # H_1: F is a family of power series
    h1 = True
    try:
        for k in range(1, 5):
            for n in range(5):
                val = a(k, n)
                if not isinstance(val, (int, float, complex)):
                    h1 = False
    except Exception:
        h1 = False

    # H_2: There exists M > 0 such that |a_n| <= M for all n >= 0 and all f in F
    h2 = True
    try:
        if M <= 0:
            h2 = False
        else:
            for k in range(1, 50):
                for n in range(50):
                    if abs(a(k, n)) > M:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: F is not uniformly equicontinuous on K
    # We verify that for m = 100, 200, 300, the distance |x_m - y_m| goes to 0,
    # but the difference |f_{k_m}(x_m) - f_{k_m}(y_m)| remains >= epsilon.
    neg_q = True
    try:
        if epsilon < 1e-3:
            neg_q = False
        
        for m in [100, 200, 300]:
            xm = x_seq(m)
            ym = y_seq(m)
            km = k_seq(m)
            
            # Check if points are within the interval K
            if xm < K[0] or xm > K[1]:
                neg_q = False
            if ym < K[0] or ym > K[1]:
                neg_q = False
                
            # Check that the distance between points is getting small
            if abs(xm - ym) > 10.0 / math.sqrt(m):
                neg_q = False
                
            # Evaluate the power series up to a sufficiently large N
            # Cap N at 100000 to prevent hanging on unreasonable witnesses
            N = min(100000, max(10000, km + 100))
            fx = sum(a(km, n) * (xm ** n) for n in range(N))
            fy = sum(a(km, n) * (ym ** n) for n in range(N))
            
            # Check if the difference is bounded away from 0 by epsilon
            if abs(fx - fy) < epsilon - 1e-7:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a family of power series",
    "H_2: There exists M > 0 such that |a_n| <= M for all n >= 0 and all f in F",
    "¬Q: F is not uniformly equicontinuous on K"
]

N_HYP = 2
NEG_Q_INDEX = 2