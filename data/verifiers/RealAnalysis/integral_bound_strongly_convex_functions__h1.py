import sympy
from sympy.abc import x

def conditions(witness):
    try:
        local_dict = {'x': x}
        if isinstance(witness, dict):
            f = sympy.sympify(witness.get('f'), locals=local_dict)
            a = sympy.sympify(witness.get('a'), locals=local_dict)
            b = sympy.sympify(witness.get('b'), locals=local_dict)
            m = sympy.sympify(witness.get('m'), locals=local_dict)
        else:
            f = sympy.sympify(witness[0], locals=local_dict)
            a = sympy.sympify(witness[1], locals=local_dict)
            b = sympy.sympify(witness[2], locals=local_dict)
            m = sympy.sympify(witness[3], locals=local_dict)
            
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) > 1:
            if x in free_syms:
                var = x
            else:
                var = list(free_syms)[0]
        else:
            var = x
            
    except Exception:
        return [False, False]

    # H1: m > 0 and f''(x) >= m for all x in the interval
    try:
        m_gt_0 = bool(m > 0)
        f2 = sympy.diff(f, var, 2)
        diff_expr = sympy.simplify(f2 - m)
        
        if var not in diff_expr.free_symbols:
            f2_ge_m = bool(diff_expr >= 0)
        else:
            f3 = sympy.diff(f2, var)
            crit_points = sympy.solve(f3, var)
            min_a_b = sympy.Min(a, b)
            max_a_b = sympy.Max(a, b)
            points_to_check = [min_a_b, max_a_b]
            for cp in crit_points:
                try:
                    if bool(cp >= min_a_b) and bool(cp <= max_a_b):
                        points_to_check.append(cp)
                except Exception:
                    pass
            
            vals = []
            for p in points_to_check:
                val = sympy.simplify(f2.subs(var, p))
                try:
                    if val.is_real is not False:
                        vals.append(val)
                except Exception:
                    pass
            if not vals:
                f2_ge_m = False
            else:
                min_val = sympy.Min(*vals)
                f2_ge_m = bool(min_val >= m)
                
        h1_ok = m_gt_0 and f2_ge_m
    except Exception:
        h1_ok = False

    # ¬Q: \int_a^b f(x) dx < f((a+b)/2)*(b-a) + m/24 * (b-a)^3
    try:
        lhs = sympy.integrate(f, (var, a, b))
        mid = sympy.Rational(1, 2) * (a + b)
        f_mid = f.subs(var, mid)
        rhs = f_mid * (b - a) + sympy.Rational(1, 24) * m * (b - a)**3
        
        neg_q_ok = bool(sympy.simplify(lhs - rhs) < 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: m > 0 and second derivative of f >= m for all x between a and b",
    "¬Q: integral of f from a to b < f((a+b)/2)*(b-a) + m/24 * (b-a)^3"
]

N_HYP = 1
NEG_Q_INDEX = 1