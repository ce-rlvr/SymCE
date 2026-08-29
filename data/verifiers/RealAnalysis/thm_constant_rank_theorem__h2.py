import sympy
from sympy import Symbol, diff, limit, Matrix, S, oo, Interval, ProductSet

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        n = witness['n']
        m = witness['m']
        k = witness['k']
        vars = witness['vars']
        f = witness['f']
        U = witness['U']
    except Exception:
        return [False, False, False]

    # H1: U is an open subset of R^n
    try:
        h1 = U.is_open
        if h1 is None:
            if isinstance(U, Interval):
                h1 = U.left_open and U.right_open
            elif isinstance(U, ProductSet):
                h1 = all(isinstance(s, Interval) and s.left_open and s.right_open for s in U.sets)
            else:
                h1 = False
    except Exception:
        h1 = False

    # H2: Jacobian has constant rank k on U
    try:
        h2 = True
        pts = []
        if 'singularities' in witness:
            pts.extend(witness['singularities'])
        
        if isinstance(U, Interval):
            intervals = [U]
        elif isinstance(U, ProductSet):
            intervals = U.sets
        else:
            intervals = []
            
        # Generate deterministic test points inside U
        for k_idx in range(5):
            pt = {}
            valid = True
            for i, var in enumerate(vars):
                if i < len(intervals) and isinstance(intervals[i], Interval):
                    inf = intervals[i].inf if intervals[i].inf != -oo else sympy.Rational(-10)
                    sup = intervals[i].sup if intervals[i].sup != oo else sympy.Rational(10)
                    frac = sympy.Rational(k_idx + 1, 6)
                    pt[var] = inf + (sup - inf) * frac
                else:
                    valid = False
            if valid:
                pts.append(pt)
                
        if not pts:
            h2 = False

        for pt in pts:
            J = []
            for i in range(m):
                row = []
                for j in range(n):
                    var = vars[j]
                    expr = f[i]
                    try:
                        df = diff(expr, var)
                        df_val = df.subs(pt)
                        if (df_val.has(S.NaN) or df_val.has(oo) or df_val.has(-oo) or 
                            df_val.has(sympy.zoo) or df_val.has(sympy.I) or df_val.has(sympy.Derivative)):
                            raise ValueError
                        diff_val = df_val
                    except Exception:
                        # Fallback to limit definition of derivative
                        h = Symbol('h')
                        expr_pt = expr.subs({v: pt[v] for v in vars if v != var})
                        val_pt = expr_pt.subs(var, pt[var])
                        val_h = expr_pt.subs(var, pt[var] + h)
                        diff_val_plus = limit((val_h - val_pt)/h, h, 0, dir='+')
                        diff_val_minus = limit((val_h - val_pt)/h, h, 0, dir='-')
                        
                        if (diff_val_plus != diff_val_minus or diff_val_plus.has(S.NaN) or 
                            diff_val_plus.has(sympy.I) or diff_val_plus.has(oo) or 
                            diff_val_plus.has(-oo) or diff_val_plus.has(sympy.zoo)):
                            h2 = False
                            break
                        diff_val = diff_val_plus
                    row.append(diff_val)
                if not h2:
                    break
            if not h2:
                break
            
            rank = Matrix(J).rank()
            if rank != k:
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails (e.g., f is not C1, so it cannot be locally diffeomorphic to a linear map)
    try:
        neg_q = False
        if 'singularities' in witness:
            for pt in witness['singularities']:
                for i in range(m):
                    for j in range(n):
                        var = vars[j]
                        expr = f[i]
                        df = diff(expr, var)
                        df_pt = df.subs({v: pt[v] for v in vars if v != var})
                        
                        # Check if the derivative is continuous at the singularity
                        lim_val_plus = limit(df_pt, var, pt[var], dir='+')
                        lim_val_minus = limit(df_pt, var, pt[var], dir='-')
                        
                        h = Symbol('h')
                        expr_pt = expr.subs({v: pt[v] for v in vars if v != var})
                        val_pt = expr_pt.subs(var, pt[var])
                        val_h = expr_pt.subs(var, pt[var] + h)
                        actual_diff = limit((val_h - val_pt)/h, h, 0, dir='+')
                        
                        if lim_val_plus != actual_diff or lim_val_minus != actual_diff:
                            neg_q = True
                            break
                    if neg_q:
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: Jacobian matrix Df(x) has constant rank k for all x in U",
    "¬Q: The conclusion fails (f is not locally diffeomorphic to a linear map, e.g., f is not C1)"
]

N_HYP = 2
NEG_Q_INDEX = 2