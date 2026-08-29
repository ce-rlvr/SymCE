import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

x = sympy.Symbol('x')

def conditions(witness):
    """
    witness is expected to be a dictionary with keys:
      'a': float, lower bound of interval X
      'b': float, upper bound of interval X
      'f': callable or sympy expression, the function f: X -> R
      'L': float, Lipschitz constant
      'D': float, diameter bound
      'alpha': float, Hölder exponent
    """
    try:
        a = float(witness['a'])
        b = float(witness['b'])
        L = float(witness['L'])
        D = float(witness['D'])
        alpha = float(witness['alpha'])
        f_input = witness['f']
        
        if not callable(f_input):
            f_input = sympy.sympify(f_input)
            
        if isinstance(f_input, sympy.Expr):
            syms = list(f_input.free_symbols)
            sym = syms[0] if syms else sympy.Symbol('x')
            f = sympy.lambdify(sym, f_input, 'math')
        else:
            f = f_input
            
        # Test f evaluation
        _ = float(f(a))
    except Exception:
        return [False, False, False, False]

    # H1: X is a valid metric space (interval [a, b] with a < b)
    try:
        h1 = (a < b)
    except Exception:
        h1 = False

    # H2: The diameter of X is bounded by D > 0
    try:
        h2 = (b - a <= D + 1e-9) and (D > 0)
    except Exception:
        h2 = False

    # H3: f is L-Lipschitz continuous on X
    try:
        n = 200
        grid = [a + i * (b - a) / (n - 1) for i in range(n)]
        f_vals = [float(f(xi)) for xi in grid]
        
        h3 = True
        for i in range(n):
            xi = grid[i]
            f_xi = f_vals[i]
            for j in range(i + 1, n):
                xj = grid[j]
                f_xj = f_vals[j]
                if abs(f_xi - f_xj) > L * abs(xi - xj) + 1e-7:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: f is NOT uniformly alpha-Hölder continuous with constant L * D^(1-alpha)
    try:
        C = L * (D ** (1.0 - alpha))
        neg_q = False
        for i in range(n):
            xi = grid[i]
            f_xi = f_vals[i]
            for j in range(i + 1, n):
                xj = grid[j]
                f_xj = f_vals[j]
                if abs(f_xi - f_xj) > C * (abs(xi - xj) ** alpha) + 1e-7:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: X is a valid metric space", "H_2: The diameter of X is bounded by D > 0", "H_3: f is L-Lipschitz continuous on X", "¬Q: f is NOT uniformly alpha-Holder continuous with constant L * D^(1-alpha)"]
N_HYP = 3
NEG_Q_INDEX = 3