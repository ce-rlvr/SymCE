import sympy
from sympy.calculus.util import function_range
import math
import itertools
import functools

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should provide:
      - 'A': a sympy.Set representing the subset of R^n
      - 'f': a sympy.Expr (in terms of 'x') or a callable representing the function
      - 'n': the dimension (integer, default 1)
      - 'L': the constant L
      - 'x': the symbol used in f (optional, defaults to sympy.Symbol('x'))
    """
    if isinstance(witness, dict):
        A = witness.get('A')
        f = witness.get('f')
        n = witness.get('n', 1)
        L = witness.get('L')
        sym = witness.get('x', x)
    else:
        A = getattr(witness, 'A', None)
        f = getattr(witness, 'f', None)
        n = getattr(witness, 'n', 1)
        L = getattr(witness, 'L', None)
        sym = getattr(witness, 'x', x)

    # H1: A is a subset of R^n
    h1_ok = False
    try:
        if isinstance(A, sympy.Set):
            if n == 1:
                h1_ok = (A.is_subset(sympy.S.Reals) is not False)
            else:
                h1_ok = (A.is_subset(sympy.S.Reals ** n) is not False)
    except Exception:
        h1_ok = False

    # neg_Q: mu^*(f(A)) > L^n * mu^*(A)
    neg_q_ok = False
    try:
        if callable(f):
            f_expr = f(sym)
        else:
            f_expr = f
            
        fA = function_range(f_expr, sym, A)
        mu_fA = fA.measure
        mu_A = A.measure
        
        lhs = sympy.sympify(mu_fA)
        rhs = sympy.sympify((L**n) * mu_A)
        
        if lhs.is_infinite and not rhs.is_infinite:
            neg_q_ok = True
        elif not lhs.is_infinite and rhs.is_infinite:
            neg_q_ok = False
        else:
            neg_q_ok = bool(lhs > rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a subset of R^n",
    "¬Q: mu^*(f(A)) > L^n * mu^*(A)"
]

N_HYP = 1
NEG_Q_INDEX = 1