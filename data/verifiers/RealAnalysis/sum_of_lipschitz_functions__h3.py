import sympy as sp
from sympy.abc import x, y, z

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_var(expr):
    if not hasattr(expr, 'free_symbols'):
        return x
    free = expr.free_symbols
    if x in free:
        return x
    if free:
        return list(free)[0]
    return x

def check_lipschitz_callable(func, L, is_h2=True):
    L = float(L)
    pairs = []
    # Generate a deterministic set of test pairs
    for i in range(-100, 100):
        a = i * 1.13
        for delta in [0.01, 0.1, 0.5, 1.0, 2.5]:
            pairs.append((a, a + delta))
            pairs.append((a, a - delta))
            
    if is_h2:
        for a, b in pairs:
            try:
                val_a = float(func(a))
                val_b = float(func(b))
                if abs(val_a - val_b) > L * abs(a - b) + 1e-7:
                    return False
            except Exception:
                return False
        return True
    else:
        for a, b in pairs:
            try:
                val_a = float(func(a))
                val_b = float(func(b))
                if abs(val_a - val_b) > L * abs(a - b) + 1e-7:
                    return True
            except Exception:
                pass
        return False

def is_lipschitz_expr(expr, L):
    try:
        var = get_var(expr)
        df = sp.diff(expr, var)
        sol = sp.solveset(sp.Abs(df) > L, var, domain=sp.S.Reals)
        if sol.is_empty == True:
            return True
        elif sol.is_empty == False:
            return False
    except Exception:
        pass
    
    try:
        var = get_var(expr)
        func = sp.lambdify(var, expr, 'math')
        return check_lipschitz_callable(func, L, is_h2=True)
    except Exception:
        return False

def is_not_lipschitz_expr(expr, L):
    try:
        var = get_var(expr)
        df = sp.diff(expr, var)
        sol = sp.solveset(sp.Abs(df) > L, var, domain=sp.S.Reals)
        if sol.is_empty == True:
            return False
        elif sol.is_empty == False:
            return True
    except Exception:
        pass
    
    try:
        var = get_var(expr)
        func = sp.lambdify(var, expr, 'math')
        return check_lipschitz_callable(func, L, is_h2=False)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f', x)
            g = witness.get('g', x**2)
            L_1 = witness.get('L_1', 1)
            L_2 = witness.get('L_2', 1)
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            f = witness[0]
            g = witness[1]
            L_1 = witness[2]
            L_2 = witness[3]
        else:
            return [False, False, False]
            
        if isinstance(f, str):
            f = sp.sympify(f)
        if isinstance(g, str):
            g = sp.sympify(g)
        if isinstance(L_1, str):
            L_1 = sp.sympify(L_1)
        if isinstance(L_2, str):
            L_2 = sp.sympify(L_2)
    except Exception:
        return [False, False, False]

    # H_1: (X, d) is a metric space
    # We implicitly evaluate on R with the standard metric, which is a metric space.
    h1 = True

    # H_2: f is Lipschitz continuous with constant L_1
    try:
        L_1_float = float(L_1)
        if L_1_float < 0:
            h2 = False
        else:
            if callable(f):
                h2 = check_lipschitz_callable(f, L_1_float, is_h2=True)
            else:
                h2 = is_lipschitz_expr(f, L_1_float)
    except Exception:
        h2 = False

    # neg_Q: f + g is NOT Lipschitz continuous with constant L_1 + L_2
    try:
        L_sum = float(L_1) + float(L_2)
        if callable(f) and callable(g):
            func_sum = lambda val: f(val) + g(val)
            neg_q = check_lipschitz_callable(func_sum, L_sum, is_h2=False)
        elif not callable(f) and not callable(g):
            expr_sum = f + g
            neg_q = is_not_lipschitz_expr(expr_sum, L_sum)
        else:
            if callable(f):
                var_g = get_var(g)
                g_func = sp.lambdify(var_g, g, 'math')
                func_sum = lambda val: f(val) + g_func(val)
            else:
                var_f = get_var(f)
                f_func = sp.lambdify(var_f, f, 'math')
                func_sum = lambda val: f_func(val) + g(val)
            neg_q = check_lipschitz_callable(func_sum, L_sum, is_h2=False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: f is Lipschitz continuous with constant L_1",
    "¬Q: f + g is not Lipschitz continuous with constant L_1 + L_2"
]

N_HYP = 2
NEG_Q_INDEX = 2