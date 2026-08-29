import sympy as sp
import math

# Top-level setup for witness expressions
x, y, t, n, k, m = sp.symbols('x y t n k m')
Interval = sp.Interval
Set = sp.Set
FiniteSet = sp.FiniteSet
Reals = sp.S.Reals

def get_max_diff_num(f_n, x_sym, n_sym, E, n_val):
    try:
        h = f_n.subs(n_sym, n_val) - f_n.subs(n_sym, 2*n_val)
    except Exception:
        return 0.0
        
    points = []
    try:
        if isinstance(E, sp.Interval):
            a = float(E.start) if E.start.is_finite else -100.0
            b = float(E.end) if E.end.is_finite else 100.0
            # linear grid
            for i in range(1001):
                points.append(a + (b-a)*i/1000)
            # log grid near boundaries
            for i in range(1, 50):
                d = (b-a) * (10**(-i/5))
                points.append(a + d)
                points.append(b - d)
            # n-dependent points
            points.extend([a + (b-a)/n_val, a + (b-a)/(n_val**2), a + (b-a)/math.sqrt(n_val)])
            points.extend([b - (b-a)/n_val, b - (b-a)/(n_val**2), b - (b-a)/math.sqrt(n_val)])
            
            if not E.start.is_finite:
                points.extend([-10**k_idx for k_idx in range(1, 6)])
                points.extend([-n_val, -n_val**2, -math.sqrt(n_val)])
            if not E.end.is_finite:
                points.extend([10**k_idx for k_idx in range(1, 6)])
                points.extend([n_val, n_val**2, math.sqrt(n_val)])
                
        elif isinstance(E, sp.FiniteSet):
            points = [float(p) for p in E if p.is_finite]
        else:
            points = [0.0, 1.0, -1.0, 10.0, -10.0]
    except Exception:
        points = [0.0, 1.0, -1.0, 10.0, -10.0]
        
    # derivative sign changes to catch narrow peaks
    try:
        dh = sp.diff(h, x_sym)
        prev_sign = None
        prev_p = None
        sorted_points = sorted(list(set(points)))
        for p in sorted_points:
            try:
                val = float(dh.subs(x_sym, p))
                sign = 1 if val > 0 else -1 if val < 0 else 0
                if prev_sign is not None and sign != prev_sign and sign != 0:
                    points.append((prev_p + p)/2)
                prev_sign = sign
                prev_p = p
            except Exception:
                pass
    except Exception:
        pass

    max_val = 0.0
    for p in points:
        try:
            val = abs(float(h.subs(x_sym, p)))
            if val > max_val:
                max_val = val
        except Exception:
            pass
            
    return max_val

def conditions(witness):
    h1_ok = False
    neg_q = False
    
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 4:
                f_n, E, x_sym, n_sym = witness
            elif len(witness) == 2:
                f_n, E = witness
                free_syms = list(f_n.free_symbols)
                n_cands = [s for s in free_syms if str(s) in ['n', 'k', 'm']]
                x_cands = [s for s in free_syms if str(s) in ['x', 'y', 't']]
                n_sym = n_cands[0] if n_cands else n
                x_sym = x_cands[0] if x_cands else x
            else:
                return [False, False]
        else:
            return [False, False]
            
        # H1: (f_n) is a sequence of real-valued functions defined on a set E
        if isinstance(f_n, sp.Expr) and isinstance(E, sp.Set):
            p = None
            if isinstance(E, sp.Interval):
                a = float(E.start) if E.start.is_finite else -10.0
                b = float(E.end) if E.end.is_finite else 10.0
                p = (a + b) / 2
            elif isinstance(E, sp.FiniteSet):
                p = list(E)[0]
            else:
                p = 0.0
                
            try:
                val = complex(f_n.subs({x_sym: p, n_sym: 1}))
                if abs(val.imag) < 1e-9:
                    h1_ok = True
            except Exception:
                h1_ok = True # Fallback if evaluation fails but types are correct
                
        if not h1_ok:
            return [False, False]
            
        # ¬Q: The sequence (f_n) does NOT converge uniformly on E
        
        # 1. Symbolic pointwise convergence check
        try:
            points_to_check = []
            if isinstance(E, sp.Interval):
                points_to_check = [E.start, E.end, (E.start + E.end)/2]
            elif isinstance(E, sp.FiniteSet):
                points_to_check = list(E)
                
            for p_val in points_to_check:
                if p_val.is_finite:
                    val = f_n.subs(x_sym, p_val)
                    L = sp.limit(val, n_sym, sp.oo)
                    if L == sp.oo or L == -sp.oo or isinstance(L, sp.AccumBounds) or "sin" in str(L) or "cos" in str(L):
                        neg_q = True
                        return [h1_ok, neg_q]
        except Exception:
            pass

        # 2. Symbolic uniform Cauchy check
        try:
            dh_sym = sp.diff(f_n - f_n.subs(n_sym, 2*n_sym), x_sym)
            roots_sym = sp.solve(dh_sym, x_sym)
            
            if isinstance(E, sp.Interval):
                if E.start.is_finite: roots_sym.append(E.start)
                if E.end.is_finite: roots_sym.append(E.end)
                
            for r in roots_sym:
                try:
                    r_inf = sp.limit(r, n_sym, sp.oo)
                    if isinstance(E, sp.Interval):
                        if r_inf < E.start or r_inf > E.end:
                            continue
                    elif isinstance(E, sp.FiniteSet):
                        if r_inf not in E:
                            continue
                    
                    h_val = sp.simplify((f_n - f_n.subs(n_sym, 2*n_sym)).subs(x_sym, r))
                    L = sp.limit(sp.Abs(h_val), n_sym, sp.oo)
                    if L > 0:
                        neg_q = True
                        return [h1_ok, neg_q]
                except Exception:
                    pass
        except Exception:
            pass
            
        # 3. Numerical uniform Cauchy check
        n_values = [10, 33, 100, 333, 1000, 3333, 10001]
        max_diffs = []
        for n_val in n_values:
            md = get_max_diff_num(f_n, x_sym, n_sym, E, n_val)
            max_diffs.append(md)
            
        if len(max_diffs) >= 2:
            if max_diffs[-1] > 1e-4 and max_diffs[-1] > 0.9 * max_diffs[-2]:
                neg_q = True
                
    except Exception:
        pass
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions defined on a set E",
    "¬Q: The sequence (f_n) does NOT converge uniformly on E to any real-valued function f"
]

N_HYP = 1
NEG_Q_INDEX = 1