import sympy
import math

# Top-level setup for potential witness expressions
x, y, z, n, m, k = sympy.symbols('x y z n m k')
R = sympy.S.Reals
N = sympy.S.Naturals

def get_max_abs(g, x_sym, D, n_val):
    points = set()
    
    if isinstance(D, sympy.FiniteSet):
        for p in D:
            try: points.add(float(p))
            except Exception: pass
    else:
        # Boundaries
        if isinstance(D, sympy.Interval):
            try: points.add(float(D.start))
            except Exception: pass
            try: points.add(float(D.end))
            except Exception: pass
            if D.end == sympy.S.Infinity:
                points.add(sympy.oo)
            if D.start == sympy.S.NegativeInfinity:
                points.add(-sympy.oo)
        elif D == sympy.S.Reals:
            points.add(sympy.oo)
            points.add(-sympy.oo)
            points.add(0.0)
        
        # Default points
        for v in [-100.0, -10.0, -1.0, -0.5, 0.0, 0.5, 1.0, 10.0, 100.0]:
            points.add(v)
            
        # Grid points for finite intervals
        if isinstance(D, sympy.Interval):
            try:
                start = float(D.start)
                end = float(D.end)
                for i in range(1, 10):
                    points.add(start + i * (end - start) / 10)
            except Exception:
                pass
                
        # n-dependent points
        try:
            n_float = float(n_val)
            n_dep = [
                1/n_float, 2/n_float, 1/(n_float+1), 1/math.sqrt(n_float),
                2/math.sqrt(n_float), 1/(2*n_float),
                n_float, n_float/2, n_float**2, math.sqrt(n_float),
                -n_float, -n_float/2, -n_float**2, -math.sqrt(n_float),
                -1/n_float, -2/n_float, -1/(n_float+1), -1/math.sqrt(n_float),
                -2/math.sqrt(n_float), -1/(2*n_float)
            ]
            for nd in n_dep:
                points.add(nd)
            if isinstance(D, sympy.Interval):
                try:
                    start = float(D.start)
                    end = float(D.end)
                    length = end - start
                    for nd in n_dep:
                        if 0 < nd < 1:
                            points.add(start + nd * length)
                            points.add(end - nd * length)
                except Exception:
                    pass
        except Exception:
            pass

    # Try to find critical points
    try:
        deriv = sympy.diff(g, x_sym)
        crit = sympy.solveset(deriv, x_sym, domain=D)
        if isinstance(crit, sympy.FiniteSet):
            for c in crit:
                try: points.add(float(c))
                except Exception: pass
        elif isinstance(crit, sympy.Union):
            for arg in crit.args:
                if isinstance(arg, sympy.FiniteSet):
                    for c in arg:
                        try: points.add(float(c))
                        except Exception: pass
    except Exception:
        pass

    max_val = -1.0
    for p in points:
        try:
            in_D = D.contains(p)
            if in_D == sympy.S.false:
                continue
        except Exception:
            continue
            
        try:
            if p == sympy.oo or p == -sympy.oo:
                val_expr = sympy.Abs(g.subs(x_sym, p))
                if val_expr == sympy.oo:
                    return float('inf')
                elif val_expr.is_real:
                    val = float(val_expr)
                    if val > max_val:
                        max_val = val
                continue
                
            val = abs(float(g.subs(x_sym, p)))
            if val > max_val:
                max_val = val
        except Exception:
            try:
                val = sympy.Abs(g.subs(x_sym, p))
                if val == sympy.oo:
                    return float('inf')
            except Exception:
                pass
    return max_val

def conditions(witness):
    """
    witness: tuple (D, f_n, x, n)
    where D is a SymPy Set, f_n is a SymPy Expr, x and n are SymPy Symbols.
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        D, f_n, x_sym, n_sym = witness
    except Exception:
        return [False, False, False]
        
    # H_1: D is a set
    try:
        h1 = isinstance(D, sympy.Set)
    except Exception:
        h1 = False
        
    # H_2: f_n is a sequence of functions from D to the real numbers
    try:
        h2 = isinstance(f_n, sympy.Expr) and isinstance(x_sym, sympy.Symbol) and isinstance(n_sym, sympy.Symbol)
        if h2:
            free_syms = f_n.free_symbols
            if not free_syms.issubset({x_sym, n_sym, sympy.pi, sympy.E}):
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: (f_n) does NOT converge uniformly on D
    try:
        neg_q = False
        if h1 and h2:
            # We check if the sequence is uniformly Cauchy by evaluating the maximum difference
            # between f_n and f_{2n}, as well as f_n and f_{n+1}, for n=100 and n=400.
            # If the maximum difference does not decrease significantly, it does not converge uniformly.
            g_n = f_n - f_n.subs(n_sym, 2 * n_sym)
            h_n = f_n - f_n.subs(n_sym, n_sym + 1)
            
            g_100 = g_n.subs(n_sym, 100)
            g_400 = g_n.subs(n_sym, 400)
            h_100 = h_n.subs(n_sym, 100)
            h_400 = h_n.subs(n_sym, 400)
            
            max_g_100 = get_max_abs(g_100, x_sym, D, 100)
            max_g_400 = get_max_abs(g_400, x_sym, D, 400)
            max_h_100 = get_max_abs(h_100, x_sym, D, 100)
            max_h_400 = get_max_abs(h_400, x_sym, D, 400)
            
            def is_non_uniform(m100, m400):
                if m100 == float('inf') or m400 == float('inf'):
                    return True
                if m100 > 1e-10 and m400 >= 0.8 * m100:
                    return True
                return False
                
            if is_non_uniform(max_g_100, max_g_400) or is_non_uniform(max_h_100, max_h_400):
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: D is a set",
    "H_2: (f_n) is a sequence of functions from D to the real numbers",
    "¬Q: (f_n) does not converge uniformly on D"
]

N_HYP = 2
NEG_Q_INDEX = 2