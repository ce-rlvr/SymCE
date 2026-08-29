import sympy
import math
import itertools
import functools

x = sympy.Symbol('x', real=True)
y = sympy.Symbol('y', real=True)
z = sympy.Symbol('z', real=True)
n = sympy.Symbol('n', integer=True)

def conditions(witness):
    # H1: X is a topological space
    try:
        if isinstance(witness, dict) and 'X' in witness:
            h1 = isinstance(witness['X'], sympy.Set)
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: conv(F) is the set of all finite convex combinations
    try:
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: conv(F) is not equicontinuous on X
    neg_q = False
    try:
        X = sympy.S.Reals
        F_raw = witness
        if isinstance(witness, dict):
            X = witness.get('X', sympy.S.Reals)
            F_raw = witness.get('F', [])
            
        if callable(F_raw):
            x_sym = sympy.Symbol('x', real=True)
            df_vals = []
            for n_val in [1, 10, 100, 1000]:
                f = F_raw(n_val)
                df = sympy.diff(f, x_sym)
                max_val = 0
                for pt in [0, 1, 0.5, -1, 2]:
                    try:
                        val = abs(df.subs(x_sym, pt).evalf())
                        if val > max_val:
                            max_val = val
                    except Exception:
                        pass
                df_vals.append(max_val)
            if len(df_vals) == 4 and df_vals[-1] > 100 and df_vals[-1] > df_vals[0]:
                neg_q = True
                
        if not neg_q:
            F = []
            if isinstance(F_raw, (list, tuple, set)):
                F = list(F_raw)
            else:
                F = [F_raw]
                
            for f in F:
                if not hasattr(f, 'free_symbols'):
                    continue
                syms = list(f.free_symbols)
                if not syms:
                    continue
                x_sym = next((s for s in syms if s.name == 'x'), syms[0])
                
                try:
                    dom = sympy.calculus.util.continuous_domain(f, x_sym, X)
                    if not X.is_subset(dom):
                        neg_q = True
                        break
                except Exception:
                    pass
                    
                params = [s for s in syms if s != x_sym]
                if params:
                    try:
                        df = sympy.diff(f, x_sym)
                        test_points = [0, 1, -1, 0.5, 2, 10]
                        try:
                            if isinstance(X, sympy.Interval):
                                if X.inf.is_real and X.sup.is_real:
                                    test_points.append(float((X.inf + X.sup) / 2))
                                elif X.inf.is_real:
                                    test_points.append(float(X.inf + 1))
                                elif X.sup.is_real:
                                    test_points.append(float(X.sup - 1))
                        except Exception:
                            pass
                            
                        for p in params:
                            for pt in test_points:
                                try:
                                    if pt not in X:
                                        continue
                                except Exception:
                                    pass
                                vals = []
                                for p_val in [1, 10, 100, 1000]:
                                    try:
                                        val = df.subs({x_sym: pt, p: p_val}).evalf()
                                        vals.append(abs(val))
                                    except Exception:
                                        pass
                                if len(vals) == 4 and vals[-1] > 100 and vals[-1] > vals[0]:
                                    neg_q = True
                                    break
                            if neg_q:
                                break
                    except Exception:
                        pass
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: conv(F) is the set of all finite convex combinations",
    "¬Q: conv(F) is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2