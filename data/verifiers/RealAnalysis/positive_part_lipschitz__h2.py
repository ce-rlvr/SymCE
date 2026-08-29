import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f_expr, L = witness
            elif len(witness) == 4:
                X, d, f_expr, L = witness
            else:
                f_expr = witness[0]
                L = witness[1] if len(witness) > 1 else 1
        elif isinstance(witness, dict):
            f_expr = witness.get('f', witness.get('f_expr', 'x'))
            L = witness.get('L', 1)
        else:
            f_expr = witness
            L = 1
            
        f = sp.sympify(f_expr)
        L = float(L)
        
        # Hypotheses are structural/definitions for this conjecture
        H_1 = True
        H_2 = True
        
        # Determine the variable
        free_syms = list(f.free_symbols)
        if len(free_syms) == 1:
            sym = free_syms[0]
        elif len(free_syms) == 0:
            sym = x
        else:
            sym = free_syms[0]
            
        f_lam = sp.lambdify(sym, f, modules=['math'])
        
        # Generate evaluation points
        points = []
        for i in range(-10000, 10000):
            points.append(round(i * 0.01, 4))
        for i in range(-1000, 1000):
            points.append(round(i * 1.0, 4))
        for i in range(-100, 100):
            points.append(round(i * 10.0, 4))
            
        points = sorted(list(set(points)))
        
        valid_points = []
        f_vals = []
        for p in points:
            try:
                v = f_lam(p)
                if isinstance(v, complex):
                    continue
                if math.isfinite(v):
                    valid_points.append(p)
                    f_vals.append(max(v, 0.0))
            except Exception:
                pass
                
        neg_Q = False
        
        # Check empirical Lipschitz condition
        for i in range(len(valid_points) - 1):
            p1 = valid_points[i]
            p2 = valid_points[i+1]
            diff = abs(p1 - p2)
            if diff > 1e-7:
                ratio = abs(f_vals[i] - f_vals[i+1]) / diff
                if ratio > L + 1e-5:
                    neg_Q = True
                    break
                    
        # Check symbolic derivative as a fallback
        if not neg_Q:
            try:
                df = sp.diff(f, sym)
                df_lam = sp.lambdify(sym, df, modules=['math'])
                for p in valid_points:
                    try:
                        v = f_lam(p)
                        if v > 1e-7:  # Only where f > 0
                            grad = abs(df_lam(p))
                            if grad > L + 1e-5:
                                neg_Q = True
                                break
                    except Exception:
                        pass
            except Exception:
                pass
                
        return [H_1, H_2, neg_Q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: f^+(x) is defined as max(f(x), 0) for all x in X",
    "¬Q: The function f^+ is not L-Lipschitz continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2