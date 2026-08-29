import sympy
from sympy import symbols
from sympy.matrices import eye, zeros
import math

# Top-level setup
x, y, z, t = symbols('x y z t')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If f is differentiable at a, then the directional derivative D_v f(a) exists and equals grad f(a) . v"
    (The dropped hypothesis is that v is a unit vector).
    
    Expected witness format:
    A dictionary with keys:
      'f': sympy expression for the function
      'vars': list of sympy variables
      'a': list of coordinates for the point a
      'v': list of coordinates for the vector v
    Or a tuple (f, vars, a, v).
    """
    try:
        if isinstance(witness, dict):
            f = witness['f']
            vars = witness['vars']
            a = witness['a']
            v = witness['v']
        else:
            f, vars, a, v = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        f_expr = sympy.sympify(f)
    except Exception:
        return [False, False, False, False]
        
    # H1: U is an open set in R^n
    # We verify this by checking that the dimensions of vars, a, and v match and are > 0.
    try:
        h1 = isinstance(vars, (list, tuple)) and len(vars) > 0 and len(vars) == len(a) and len(vars) == len(v)
    except Exception:
        h1 = False
        
    # H2: f is a function from U to R
    try:
        h2 = isinstance(f_expr, sympy.Expr) and not isinstance(f_expr, sympy.MatrixBase)
    except Exception:
        h2 = False
        
    # H3: f is differentiable at a
    # We check if all partial derivatives exist and evaluate to finite real numbers at a.
    try:
        grad_vals = []
        for var in vars:
            g = sympy.diff(f_expr, var).subs(zip(vars, a))
            grad_vals.append(float(g))
        h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: The directional derivative D_v f(a) exists and equals \nabla f(a) \cdot v
    # The true directional derivative (rate of change in direction v) is grad \cdot (v / ||v||).
    # The conclusion claims it is grad \cdot v.
    # neg_Q is True if the conclusion FAILS (i.e., they are not equal, or v is the zero vector).
    try:
        v_vals = [float(vi) for vi in v]
        v_norm_sq = sum(vi**2 for vi in v_vals)
        if v_norm_sq == 0:
            # Directional derivative is undefined for the zero vector, so "exists and equals..." is False.
            neg_q = True
        else:
            v_norm = math.sqrt(v_norm_sq)
            true_Dv = sum(g * (vi / v_norm) for g, vi in zip(grad_vals, v_vals))
            claimed_Dv = sum(g * vi for g, vi in zip(grad_vals, v_vals))
            
            # The conclusion fails if the true directional derivative does not equal the claimed dot product
            neg_q = abs(true_Dv - claimed_Dv) > 1e-9
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an open set in R^n",
    "H_2: f is a function from U to R",
    "H_3: f is differentiable at a",
    "¬Q: The directional derivative D_v f(a) does not equal grad f(a) . v"
]

N_HYP = 3
NEG_Q_INDEX = 3