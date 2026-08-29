import sympy
import math

x = sympy.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is Lipschitz continuous",
    "¬Q: f is not of bounded variation"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            f, a, b = witness
        else:
            f = witness
            a = 0
            b = sympy.oo
    except Exception:
        return [False, False]
        
    # H1: f is Lipschitz continuous on [a, b]
    h1 = False
    try:
        df = sympy.diff(f, x)
        
        # 1. Check limits at infinity
        unbounded_lim = False
        try:
            if b == sympy.oo:
                if sympy.limit(sympy.Abs(df), x, sympy.oo) == sympy.oo:
                    unbounded_lim = True
            if a == -sympy.oo:
                if sympy.limit(sympy.Abs(df), x, -sympy.oo) == sympy.oo:
                    unbounded_lim = True
        except Exception:
            pass
            
        if unbounded_lim:
            h1 = False
        else:
            # 2. Try exact maximum
            sup_evaluated = False
            try:
                sup = sympy.calculus.util.maximum(sympy.Abs(df), x, sympy.Interval(a, b))
                if sup < sympy.oo:
                    h1 = True
                    sup_evaluated = True
                elif sup == sympy.oo:
                    h1 = False
                    sup_evaluated = True
            except Exception:
                pass
                
            if not sup_evaluated:
                # 3. Heuristic
                if b == sympy.oo and a != -sympy.oo:
                    pts = [a, a + 1e-5, a + 1e-3, a + 0.1] + [a + 10**i for i in range(10)] + [a + 2*10**i for i in range(10)]
                elif a == -sympy.oo and b != sympy.oo:
                    pts = [b, b - 1e-5, b - 1e-3, b - 0.1] + [b - 10**i for i in range(10)] + [b - 2*10**i for i in range(10)]
                elif a == -sympy.oo and b == sympy.oo:
                    pts = [0] + [10**i for i in range(10)] + [-10**i for i in range(10)] + [2*10**i for i in range(10)] + [-2*10**i for i in range(10)]
                else:
                    pts = [a + (b-a)*i/100.0 for i in range(101)]
                    
                vals = []
                is_unbounded = False
                for p in pts:
                    try:
                        val_expr = sympy.Abs(df).subs(x, p).evalf()
                        if val_expr == sympy.oo or val_expr == sympy.zoo:
                            is_unbounded = True
                            break
                        v = float(val_expr)
                        if math.isnan(v):
                            lim = sympy.limit(sympy.Abs(df), x, p)
                            if lim == sympy.oo or lim == sympy.zoo:
                                is_unbounded = True
                                break
                            try:
                                v_lim = float(lim.evalf())
                                if math.isnan(v_lim):
                                    is_unbounded = True
                                    break
                                vals.append(v_lim)
                            except Exception:
                                is_unbounded = True
                                break
                        else:
                            vals.append(v)
                    except Exception:
                        try:
                            lim = sympy.limit(sympy.Abs(df), x, p)
                            if lim == sympy.oo or lim == sympy.zoo:
                                is_unbounded = True
                                break
                            v_lim = float(lim.evalf())
                            if math.isnan(v_lim):
                                is_unbounded = True
                                break
                            vals.append(v_lim)
                        except Exception:
                            is_unbounded = True
                            break
                            
                if is_unbounded:
                    h1 = False
                elif vals and max(vals) > 1e6:
                    h1 = False
                else:
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: f is NOT of bounded variation on [a, b]
    neg_q = False
    try:
        df = sympy.diff(f, x)
        var_evaluated = False
        try:
            if hasattr(f, 'is_polynomial') and f.is_polynomial(x):
                var = sympy.integrate(sympy.Abs(df), (x, a, b))
                if var == sympy.oo or var == sympy.zoo:
                    neg_q = True
                    var_evaluated = True
                elif var.is_number and var.is_finite:
                    neg_q = False
                    var_evaluated = True
        except Exception:
            pass
            
        if not var_evaluated:
            # Numerical fallback
            if b == sympy.oo and a != -sympy.oo:
                v1 = 0
                try:
                    prev = float(f.subs(x, a).evalf())
                except Exception:
                    prev = float(f.subs(x, a + 1e-5).evalf())
                for i in range(1, 201):
                    curr = float(f.subs(x, a + i * 0.5).evalf())
                    v1 += abs(curr - prev)
                    prev = curr
                v2 = v1
                for i in range(201, 2001):
                    curr = float(f.subs(x, a + i * 0.5).evalf())
                    v2 += abs(curr - prev)
                    prev = curr
                neg_q = (v2 > v1 * 1.5 and v2 > 1e-3)
            elif a == -sympy.oo and b != sympy.oo:
                v1 = 0
                try:
                    prev = float(f.subs(x, b - 100).evalf())
                except Exception:
                    prev = float(f.subs(x, b - 100 + 1e-5).evalf())
                for i in range(1, 201):
                    curr = float(f.subs(x, b - 100 + i * 0.5).evalf())
                    v1 += abs(curr - prev)
                    prev = curr
                v2 = 0
                try:
                    prev = float(f.subs(x, b - 1000).evalf())
                except Exception:
                    prev = float(f.subs(x, b - 1000 + 1e-5).evalf())
                for i in range(1, 2001):
                    curr = float(f.subs(x, b - 1000 + i * 0.5).evalf())
                    v2 += abs(curr - prev)
                    prev = curr
                neg_q = (v2 > v1 * 1.5 and v2 > 1e-3)
            elif a == -sympy.oo and b == sympy.oo:
                v1 = 0
                try:
                    prev = float(f.subs(x, -50).evalf())
                except Exception:
                    prev = float(f.subs(x, -50 + 1e-5).evalf())
                for i in range(1, 201):
                    curr = float(f.subs(x, -50 + i * 0.5).evalf())
                    v1 += abs(curr - prev)
                    prev = curr
                v2 = 0
                try:
                    prev = float(f.subs(x, -500).evalf())
                except Exception:
                    prev = float(f.subs(x, -500 + 1e-5).evalf())
                for i in range(1, 2001):
                    curr = float(f.subs(x, -500 + i * 0.5).evalf())
                    v2 += abs(curr - prev)
                    prev = curr
                neg_q = (v2 > v1 * 1.5 and v2 > 1e-3)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]