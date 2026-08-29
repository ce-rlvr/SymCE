import sympy
from sympy import Matrix, Symbol, zoo, nan, oo
import math
import itertools
import functools

# Top-level setup for potential witness expressions
x, y, z, t = sympy.symbols('x y z t')

def conditions(witness) -> list[bool]:
    """
    Witness is expected to be a tuple: (vars, f, a)
    where:
      - vars is a list/tuple of sympy Symbols representing coordinates in R^n
      - f is a list/tuple of sympy Expressions representing the function f: R^n -> R^n
      - a is a list/tuple of real numbers representing the point a in R^n
    """
    try:
        vars, f, a = witness
    except Exception:
        return [False, False, False]
        
    # H_1: U is an open set in R^n (witness provides valid dimension n >= 1 and point a in R^n)
    try:
        h1 = (isinstance(vars, (list, tuple)) and 
              isinstance(f, (list, tuple)) and 
              isinstance(a, (list, tuple)) and 
              len(vars) == len(f) == len(a) and 
              len(vars) >= 1 and
              all(isinstance(v, Symbol) for v in vars) and
              all(sympy.sympify(v_a).is_real is not False for v_a in a))
    except Exception:
        h1 = False

    # H_2: f is a continuously differentiable (C^1) function
    h2 = False
    if h1:
        try:
            subs_dict = dict(zip(vars, a))
            # Check if f can be evaluated at a without singularities
            f_a = [sympy.sympify(expr).subs(subs_dict) for expr in f]
            if not any(val.has(zoo, nan, oo, -oo) for val in f_a):
                # Compute Jacobian matrix and evaluate at a
                J = Matrix(f).jacobian(vars)
                J_a = J.subs(subs_dict)
                if not any(val.has(zoo, nan, oo, -oo) for val in J_a):
                    # Ensure the Jacobian is real-valued at a
                    if all(val.is_real is not False for val in J_a):
                        h2 = True
        except Exception:
            h2 = False

    # ¬Q: f is not locally invertible with a C^1 inverse
    # By the Inverse Function Theorem and the Chain Rule, f has a local C^1 inverse 
    # if and only if its Jacobian matrix at a is invertible (determinant != 0).
    # Therefore, the conclusion fails exactly when det(J_f(a)) == 0.
    neg_q = False
    if h2:
        try:
            det_J = sympy.simplify(J_a.det())
            try:
                # Handle floating point evaluation safely
                neg_q = abs(float(det_J)) < 1e-12
            except TypeError:
                # Fallback for exact symbolic expressions
                neg_q = (det_J == 0)
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open set in R^n",
    "H_2: f is a continuously differentiable (C^1) function",
    "¬Q: f is not locally invertible with a C^1 inverse"
]

N_HYP = 2
NEG_Q_INDEX = 2