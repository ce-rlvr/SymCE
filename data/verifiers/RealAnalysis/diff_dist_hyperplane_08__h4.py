import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def to_list(v):
    """Helper to flatten vectors/matrices into a standard list."""
    if hasattr(v, 'tolist'):
        res = v.tolist()
        while res and isinstance(res[0], list):
            res = [item for sublist in res for item in sublist]
        return res
    return list(v)

def conditions(witness) -> list[bool]:
    try:
        a, b, x0 = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: a in R^n is a non-zero vector and b in R
    try:
        a_list = to_list(a)
        is_vec_a = len(a_list) > 0 and all(
            isinstance(x, (int, float)) or (hasattr(x, 'is_real') and x.is_real) 
            for x in a_list
        )
        is_scalar_b = isinstance(b, (int, float)) or (hasattr(b, 'is_real') and b.is_real)
        
        is_nonzero_a = False
        if is_vec_a:
            for x in a_list:
                try:
                    if abs(float(x)) > 1e-12:
                        is_nonzero_a = True
                        break
                except Exception:
                    if sympy.simplify(x) != 0:
                        is_nonzero_a = True
                        break
                        
        h1 = bool(is_vec_a and is_scalar_b and is_nonzero_a)
    except Exception:
        h1 = False

    # H_2: H = {x in R^n : a.x = b} is a hyperplane
    # This is true by definition as long as 'a' is a valid non-zero vector.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H_3: f: R^n -> R is defined by f(x) = |a.x - b| / ||a||_2
    # This means x0 must be a valid vector in R^n (same dimension as a).
    try:
        x0_list = to_list(x0)
        is_vec_x0 = len(x0_list) == len(a_list) and all(
            isinstance(x, (int, float)) or (hasattr(x, 'is_real') and x.is_real) 
            for x in x0_list
        )
        h3 = bool(is_vec_x0)
    except Exception:
        h3 = False

    # ¬Q: f is not differentiable at x_0
    # The function f(x) = |a.x - b| / ||a||_2 is not differentiable 
    # if and only if the argument to the absolute value is zero (since a != 0).
    try:
        if h1 and h3:
            dot_product = sum(x * y for x, y in zip(a_list, x0_list))
            diff = dot_product - b
            try:
                diff_float = float(diff)
                neg_q = abs(diff_float) < 1e-12
            except Exception:
                neg_q = bool(sympy.simplify(diff) == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a in R^n is a non-zero vector and b in R",
    "H_2: H = {x in R^n : a.x = b} is a hyperplane",
    "H_3: f: R^n -> R is defined by f(x) = |a.x - b| / ||a||_2",
    "¬Q: f is not differentiable at x_0"
]

N_HYP = 3
NEG_Q_INDEX = 3