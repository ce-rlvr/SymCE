import sympy as sp
from sympy.calculus.util import continuous_domain, maximum, minimum

CONDITION_LABELS = [
    "H_1: f is continuously differentiable on interval a to b",
    "H_2: There exists a real number M such that abs(df/dx) <= M for all x in interval a to b",
    "H_3: n is a positive integer",
    "H_4: L_n is the left Riemann sum approximation of int_a^b f(x)dx with n equal subintervals",
    "¬Q: abs(int_a^b f(x)dx - L_n) > M(b-a)^2 / (2n)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = sp.sympify(witness['f'])
            a = sp.sympify(witness['a'])
            b = sp.sympify(witness['b'])
            M = sp.sympify(witness['M'])
            n = witness['n']
            L_n = witness.get('L_n', witness.get('Ln', None))
            if L_n is not None:
                L_n = sp.sympify(L_n)
        else:
            if len(witness) == 6:
                f, a, b, M, n, L_n = witness
                f = sp.sympify(f)
                a = sp.sympify(a)
                b = sp.sympify(b)
                M = sp.sympify(M)
                L_n = sp.sympify(L_n)
            elif len(witness) == 5:
                f, a, b, M, n = witness
                f = sp.sympify(f)
                a = sp.sympify(a)
                b = sp.sympify(b)
                M = sp.sympify(M)
                L_n = None
            else:
                return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    try:
        free_syms = list(f.free_symbols) if hasattr(f, 'free_symbols') else []
        if len(free_syms) == 1:
            var = free_syms[0]
        elif len(free_syms) > 1:
            var = sp.Symbol('x')
            if var not in free_syms:
                var = free_syms[0]
        else:
            var = sp.Symbol('x')
    except Exception:
        var = sp.Symbol('x')

    try:
        is_empty = float(a) > float(b)
    except Exception:
        is_empty = False

    try:
        if is_empty:
            H1 = True
        else:
            df = sp.diff(f, var)
            if df.is_polynomial(var):
                H1 = True
            else:
                try:
                    dom = continuous_domain(df, var, sp.Interval(a, b))
                    H1 = (dom == sp.Interval(a, b))
                except Exception:
                    H1 = True
    except Exception:
        H1 = False

    try:
        if is_empty:
            H2 = True
        else:
            df = sp.diff(f, var)
            try:
                max_val = maximum(df, var, sp.Interval(a, b))
                min_val = minimum(df, var, sp.Interval(a, b))
            except Exception:
                max_val = None
                min_val = None
            
            def is_le(val, M_val):
                if val is None:
                    return False
                try:
                    diff = sp.simplify(val - M_val)
                    return float(diff) <= 1e-12
                except Exception:
                    return False
                    
            H2 = is_le(max_val, M) and is_le(-min_val, M)
    except Exception:
        H2 = False

    try:
        H3 = False
        if isinstance(n, int):
            H3 = n > 0
        elif isinstance(n, float):
            H3 = n.is_integer() and n > 0
        elif hasattr(n, 'is_Integer') and n.is_Integer:
            H3 = n > 0
        elif isinstance(n, sp.Expr):
            H3 = bool(n.is_integer and n.is_positive)
    except Exception:
        H3 = False

    try:
        if not H3:
            H4 = False
            L_n_val = None
        else:
            dx = sp.simplify((b - a) / sp.S(n))
            expected_Ln = sum(f.subs(var, a + i * dx) for i in range(int(n))) * dx
            if L_n is not None:
                diff = sp.simplify(L_n - expected_Ln)
                try:
                    H4 = abs(float(diff)) < 1e-9
                except Exception:
                    H4 = (diff == 0)
                L_n_val = L_n
            else:
                H4 = True
                L_n_val = expected_Ln
    except Exception:
        H4 = False
        L_n_val = None

    try:
        if not H3 or L_n_val is None:
            neg_Q = False
        else:
            integral_val = sp.integrate(f, (var, a, b))
            error = sp.Abs(integral_val - L_n_val)
            bound = M * (b - a)**2 / (2 * sp.S(n))
            
            diff = sp.simplify(error - bound)
            try:
                val = float(diff)
                neg_Q = val > 1e-12
            except Exception:
                if diff.is_positive:
                    neg_Q = True
                else:
                    neg_Q = False
    except Exception:
        neg_Q = False

    return [bool(H1), bool(H2), bool(H3), bool(H4), bool(neg_Q)]