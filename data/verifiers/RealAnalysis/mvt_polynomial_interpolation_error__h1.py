import sympy
import math

t = sympy.Symbol('t', real=True)
x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        f = witness['f']
        a = witness['a']
        b = witness['b']
        X = witness['X']
        P = witness['P']
        x_pt = witness['x']
    except KeyError:
        return [False, False, False, False]

    # Parse f
    if callable(f):
        try:
            f_expr = f(t)
        except Exception:
            f_expr = sympy.sympify(f)
    else:
        f_expr = sympy.sympify(f)

    # Parse P
    if callable(P):
        try:
            P_expr = P(t)
        except Exception:
            P_expr = sympy.sympify(P)
    else:
        P_expr = sympy.sympify(P)

    # Determine the variable used in the expressions
    free_syms = f_expr.free_symbols | P_expr.free_symbols
    if len(free_syms) == 1:
        var = list(free_syms)[0]
    elif len(free_syms) > 1:
        sym_names = {s.name: s for s in free_syms}
        if 'x' in sym_names:
            var = sym_names['x']
        elif 't' in sym_names:
            var = sym_names['t']
        else:
            var = list(free_syms)[0]
    else:
        var = t

    # H1: x_1, ..., x_n are distinct points in interval
    try:
        n = len(X)
        unique_X = []
        for xi in X:
            is_unique = True
            for u in unique_X:
                if sympy.simplify(xi - u) == 0:
                    is_unique = False
                    break
            if is_unique:
                unique_X.append(xi)
        h1 = (n > 0) and (len(unique_X) == n)
        if h1:
            for xi in X:
                if not (float(a) <= float(xi) <= float(b)):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: P is the unique polynomial of degree at most n-1 interpolating f at x_1, ..., x_n
    try:
        is_poly = P_expr.is_polynomial(var)
        if is_poly is not False:
            deg = sympy.degree(P_expr, var)
            h2 = (deg <= n - 1)
        else:
            h2 = False
            
        if h2:
            for xi in X:
                val_P = P_expr.subs(var, xi)
                val_f = f_expr.subs(var, xi)
                if sympy.simplify(val_P - val_f) != 0:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H3: x is a point in interval distinct from x_1, ..., x_n
    try:
        h3 = (float(a) <= float(x_pt) <= float(b))
        if h3:
            for xi in X:
                if sympy.simplify(x_pt - xi) == 0:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # Negated Conclusion: There does NOT exist c in (min, max) satisfying the error formula
    try:
        pts = [x_pt] + X
        m = min(pts, key=lambda pt: float(pt))
        M = max(pts, key=lambda pt: float(pt))
        
        V = sympy.simplify(f_expr.subs(var, x_pt) - P_expr.subs(var, x_pt))
        
        prod = 1
        for xi in X:
            prod *= (x_pt - xi)
        
        W = sympy.simplify(prod / math.factorial(n))
        
        target_deriv = sympy.simplify(V / W)
        
        dnf = sympy.diff(f_expr, var, n)
        eq = sympy.simplify(dnf - target_deriv)
        
        eq_free = eq.free_symbols
        if var not in eq_free:
            neg_q = (abs(float(eq)) > 1e-9)
        else:
            sols = sympy.solveset(eq, var, domain=sympy.Interval.open(float(m), float(M)))
            if sols == sympy.EmptySet:
                neg_q = True
            elif isinstance(sols, sympy.Set) and sols.is_empty == False and not isinstance(sols, sympy.ConditionSet):
                neg_q = False
            else:
                has_root = False
                fm = float(m)
                fM = float(M)
                steps = 1000
                
                use_subs = False
                try:
                    f_num = sympy.lambdify(var, eq, modules=['math'])
                    f_num(fm + (fM - fm) / 2)
                except Exception:
                    use_subs = True

                if not use_subs:
                    for i in range(1, steps):
                        pt = fm + (fM - fm) * i / steps
                        try:
                            v = f_num(pt)
                            if abs(v) <= 1e-7:
                                has_root = True
                                break
                        except Exception:
                            pass
                else:
                    for i in range(1, steps):
                        pt = fm + (fM - fm) * i / steps
                        try:
                            v = float(eq.subs(var, pt))
                            if abs(v) <= 1e-7:
                                has_root = True
                                break
                        except Exception:
                            pass
                neg_q = not has_root
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x_1 to x_n are distinct points in the interval",
    "H_2: P is the unique polynomial of degree at most n-1 interpolating f",
    "H_3: x is a point in the interval distinct from x_1 to x_n",
    "¬Q: There does not exist c in the open interval satisfying the error formula"
]

N_HYP = 3
NEG_Q_INDEX = 3