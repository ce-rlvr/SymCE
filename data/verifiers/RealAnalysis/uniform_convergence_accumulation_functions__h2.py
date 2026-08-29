import sympy as sp
import math

x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True, positive=True)
t = sp.Symbol('t', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f_n_expr = sp.sympify(witness.get('f_n'))
            f_expr = sp.sympify(witness.get('f')) if witness.get('f') is not None else None
            F_n_expr = sp.sympify(witness.get('F_n')) if witness.get('F_n') is not None else None
            F_expr = sp.sympify(witness.get('F')) if witness.get('F') is not None else None
            a_val = float(sp.sympify(witness.get('a')))
            b_val = float(sp.sympify(witness.get('b')))
        else:
            if len(witness) == 6:
                f_n_expr = sp.sympify(witness[0])
                f_expr = sp.sympify(witness[1])
                F_n_expr = sp.sympify(witness[2])
                F_expr = sp.sympify(witness[3])
                a_val = float(sp.sympify(witness[4]))
                b_val = float(sp.sympify(witness[5]))
            elif len(witness) == 3:
                f_n_expr = sp.sympify(witness[0])
                f_expr = F_n_expr = F_expr = None
                a_val = float(sp.sympify(witness[1]))
                b_val = float(sp.sympify(witness[2]))
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    if a_val >= b_val:
        return [False, False, False]

    # H1: f_n is Riemann integrable on the interval
    h1_ok = False
    try:
        mid = a_val + 0.5 * (b_val - a_val)
        v = complex(f_n_expr.subs({n: 2, x: mid}))
        if not math.isnan(v.real):
            h1_ok = True
    except Exception:
        pass

    # H2: F_n is the integral of f_n
    h2_ok = False
    try:
        if F_n_expr is None:
            F_n_expr = sp.integrate(f_n_expr.subs(x, t), (t, a_val, x))
            h2_ok = True
        else:
            dF = sp.diff(F_n_expr, x)
            match = True
            for n_val in [3, 7]:
                for x_val in [a_val + 0.2*(b_val-a_val), a_val + 0.7*(b_val-a_val)]:
                    v1 = complex(dF.subs({n: n_val, x: x_val}))
                    v2 = complex(f_n_expr.subs({n: n_val, x: x_val}))
                    if abs(v1 - v2) > 1e-3:
                        match = False
                        break
            v_a = complex(F_n_expr.subs({n: 5, x: a_val}))
            if abs(v_a) > 1e-3:
                match = False
            h2_ok = match
    except Exception:
        pass

    # Neg_Q: F_n does NOT converge uniformly to F
    neg_q_ok = False
    try:
        if f_expr is None:
            f_expr = sp.limit(f_n_expr, n, sp.oo)
        
        if F_expr is None:
            F_expr = sp.integrate(f_expr.subs(x, t), (t, a_val, x))
        
        def get_max_diff(n_val):
            pts = [a_val, b_val]
            for i in range(1, 50):
                pts.append(a_val + i * (b_val - a_val) / 50)
            for p in [0.5, 1.0, 1.5, 2.0]:
                for c in [0.1, 1.0, 5.0]:
                    d = c * (b_val - a_val) / (n_val ** p)
                    if a_val <= a_val + d <= b_val:
                        pts.append(a_val + d)
                    if a_val <= b_val - d <= b_val:
                        pts.append(b_val - d)
            
            m_diff = 0.0
            for pt in pts:
                try:
                    val_Fn = complex(F_n_expr.subs({n: n_val, x: pt}))
                    val_F = complex(F_expr.subs({x: pt}))
                    diff = abs(val_Fn - val_F)
                    if diff > m_diff:
                        m_diff = diff
                except Exception:
                    continue
            return m_diff

        diff_100 = get_max_diff(100)
        diff_500 = get_max_diff(500)

        if diff_500 > 0.01 and diff_500 >= 0.5 * diff_100:
            neg_q_ok = True
            
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f_n is a sequence of Riemann integrable functions",
    "H_2: F_n is the integral of f_n",
    "not_Q: F_n does not converge uniformly to F"
]

N_HYP = 2
NEG_Q_INDEX = 2