import sympy
from sympy import Symbol, Interval, integrate, minimum, maximum
import math

x = Symbol('x', real=True)

def conditions(witness):
    x_sym = Symbol('x', real=True)
    if isinstance(witness, (tuple, list)):
        if len(witness) == 4:
            f, a, b, P = witness
            if hasattr(f, 'free_symbols'):
                syms = list(f.free_symbols)
                if len(syms) >= 1:
                    x_sym = syms[0]
        elif len(witness) == 5:
            f, x_sym, a, b, P = witness
        else:
            return [False] * 5
    elif isinstance(witness, dict):
        f = witness.get('f')
        a = witness.get('a')
        b = witness.get('b')
        P = witness.get('P')
        x_sym = witness.get('x', Symbol('x', real=True))
        if f is None or a is None or b is None or P is None:
            return [False] * 5
    else:
        return [False] * 5

    if isinstance(f, (int, float)):
        f = sympy.sympify(f)

    # H1: f is a bounded real-valued function defined on the interval
    h1 = False
    try:
        a_f = float(a)
        b_f = float(b)
        if hasattr(f, 'subs'):
            m = minimum(f, x_sym, Interval(a_f, b_f))
            M = maximum(f, x_sym, Interval(a_f, b_f))
            if m.is_number and M.is_number:
                if m.is_finite and M.is_finite:
                    h1 = True
            else:
                raise ValueError
        else:
            raise ValueError
    except Exception:
        # fallback to sampling
        try:
            vals = []
            step = (b_f - a_f) / 100.0
            for i in range(101):
                v = a_f + i * step
                if hasattr(f, 'subs'):
                    val = float(f.subs(x_sym, v))
                else:
                    val = float(f(v))
                vals.append(val)
            if all(math.isfinite(v) for v in vals):
                h1 = True
        except Exception:
            pass

    # H2: P is a partition of the interval
    h2 = False
    try:
        P_f = [float(p) for p in P]
        if len(P_f) >= 2:
            if math.isclose(P_f[0], float(a)) and math.isclose(P_f[-1], float(b)):
                if all(P_f[i] < P_f[i+1] for i in range(len(P_f)-1)):
                    h2 = True
    except Exception:
        pass

    # H3 and H4: L and U are the Darboux sums
    h3 = True
    h4 = True

    computed_L = 0.0
    computed_U = 0.0
    L_U_success = False
    try:
        P_f = [float(p) for p in P]
        for i in range(len(P_f)-1):
            A, B = P_f[i], P_f[i+1]
            m_val = None
            M_val = None
            if hasattr(f, 'subs'):
                try:
                    m = minimum(f, x_sym, Interval(A, B))
                    M = maximum(f, x_sym, Interval(A, B))
                    if m.is_number and M.is_number and m.is_finite and M.is_finite:
                        m_val = float(m)
                        M_val = float(M)
                except Exception:
                    pass
            if m_val is None or M_val is None:
                vals = []
                step = (B - A) / 100.0
                for j in range(101):
                    v = A + j * step
                    if hasattr(f, 'subs'):
                        val = float(f.subs(x_sym, v))
                    else:
                        val = float(f(v))
                    vals.append(val)
                m_val = min(vals)
                M_val = max(vals)
            
            computed_L += m_val * (B - A)
            computed_U += M_val * (B - A)
        L_U_success = True
    except Exception:
        pass

    # Conclusion: L <= int f <= U
    neg_q = False
    try:
        I_val = None
        if hasattr(f, 'subs'):
            I = integrate(f, (x_sym, a, b))
            if I.has(sympy.Integral):
                I_eval = I.evalf()
                if I_eval.is_number:
                    I_val = float(I_eval)
                else:
                    neg_q = True
            else:
                I_val = float(I)
        elif callable(f):
            neg_q = False
            
        if I_val is not None:
            if math.isnan(I_val) or math.isinf(I_val):
                neg_q = True
            elif L_U_success:
                eps = 1e-7
                if not (computed_L - eps <= I_val <= computed_U + eps):
                    neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f is a bounded real-valued function defined on the interval",
    "H_2: P is a partition of the interval",
    "H_3: L is the lower Darboux sum of f with respect to P",
    "H_4: U is the upper Darboux sum of f with respect to P",
    "not Q: The integral is not bounded by the Darboux sums or is undefined"
]

N_HYP = 4
NEG_Q_INDEX = 4