import sympy as sp

# Top-level setup
t = sp.Symbol('t', real=True)

CONDITION_LABELS = [
    "H_1: X is a Banach space",
    "H_2: x and y are distinct points in X",
    "¬Q: There is no c in (x, y) such that f(y) - f(x) in \\langle \\partial f(c), y - x \\rangle"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample.
    
    The witness is expected to be a tuple or dict: (f_expr, val_x, val_y, x_val, y_val)
    - f_expr: a sympy expression representing f(t) for t strictly in the open interval (x_val, y_val).
    - val_x: the value of f at x_val.
    - val_y: the value of f at y_val.
    - x_val, y_val: the distinct points x and y in R.
    
    Example of a valid counterexample witness:
    f(t) = t on (0, 1), f(0) = 1, f(1) = 0
    Witness: ('t', 1, 0, 0, 1)
    """
    try:
        if isinstance(witness, dict):
            f_expr = witness['f_expr']
            val_x = witness['val_x']
            val_y = witness['val_y']
            x_val = witness['x_val']
            y_val = witness['y_val']
        else:
            if len(witness) != 5:
                return [False, False, False]
            f_expr, val_x, val_y, x_val, y_val = witness
            
        f_expr = sp.sympify(f_expr)
        val_x = sp.sympify(val_x)
        val_y = sp.sympify(val_y)
        x_val = sp.sympify(x_val)
        y_val = sp.sympify(y_val)
        
        # Identify the variable
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = sp.Symbol('t', real=True)
        else:
            return [False, False, False]
            
        # H_1: X is a Banach space
        # We are working in R, which is a Banach space.
        h1 = True
        
        # H_2: x and y are distinct points in X
        h2 = bool(sp.simplify(x_val - y_val) != 0)
        
        # neg_Q: The conclusion fails.
        # Conclusion: exists c in (x, y) such that f(y) - f(x) in \partial f(c) * (y - x)
        # Since f_expr is the expression on the open interval, we assume it is continuously differentiable there.
        # Thus \partial f(c) = { f'(c) }.
        # We check if there is NO c in (x, y) satisfying val_y - val_x = f'(c) * (y_val - x_val).
        
        df = sp.diff(f_expr, var)
        
        # The equation to solve: df(c) * (y_val - x_val) == val_y - val_x
        lhs = df * (y_val - x_val)
        rhs = val_y - val_x
        
        eq = sp.Eq(lhs, rhs)
        
        # Domain is the open interval between x_val and y_val
        domain = sp.Interval(sp.Min(x_val, y_val), sp.Max(x_val, y_val), left_open=True, right_open=True)
        
        sols = sp.solveset(eq, var, domain=domain)
        
        neg_q = (sols == sp.EmptySet)
        
    except Exception:
        return [False, False, False]
        
    return [h1, h2, neg_q]