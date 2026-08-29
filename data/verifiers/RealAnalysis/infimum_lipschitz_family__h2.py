import sympy
import math

# Top-level setup for witness expressions
x = sympy.Symbol('x', real=True)
Interval = sympy.Interval
oo = sympy.oo
Reals = sympy.S.Reals

def conditions(witness) -> list[bool]:
    # Parse witness: can be a single expression, a list of expressions, 
    # or a tuple (domain, list_of_expressions)
    domain = sympy.S.Reals
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], sympy.Set):
        domain, F_raw = witness
        if isinstance(F_raw, list) or isinstance(F_raw, tuple):
            F = list(F_raw)
        else:
            F = [F_raw]
    else:
        if isinstance(witness, list) or isinstance(witness, tuple):
            F = list(witness)
        else:
            F = [witness]
            
    # H_1: F is a family of functions from a metric space (X, d) to the real numbers
    try:
        h1 = len(F) > 0 and all(isinstance(f, sympy.Expr) for f in F)
    except Exception:
        h1 = False
        
    # H_2: There exists at least one point x_0 in X such that the infimum over f in F of f(x_0) is a finite real number
    h2 = False
    try:
        def is_in_domain_h2(val):
            try:
                if domain == sympy.S.Reals:
                    return True
                return domain.contains(val) == sympy.S.true
            except Exception:
                return True

        for x0 in [0, 1, -1, 2, -2, sympy.pi, sympy.E]:
            if is_in_domain_h2(x0):
                vals = [float(f.subs(x, x0)) for f in F]
                inf_val = min(vals)
                if not math.isinf(inf_val) and not math.isnan(inf_val):
                    h2 = True
                    break
    except Exception:
        pass

    # neg_Q: The pointwise infimum function g(x) = \inf_{f \in F} f(x) is NOT L-Lipschitz continuous on X
    neg_q = False
    try:
        def g(v):
            return min(float(f.subs(x, v)) for f in F)
            
        def is_in_domain(val):
            try:
                if domain == sympy.S.Reals:
                    return True
                return domain.contains(val) == sympy.S.true
            except Exception:
                return True

        def is_unbounded(slopes):
            if len(slopes) < 3:
                return False
            increasing = all(slopes[i+1] > slopes[i] - 1e-5 for i in range(len(slopes)-1))
            large = slopes[-1] > 1000
            ratio = slopes[-1] / (slopes[0] + 1e-9) > 100
            return increasing and large and ratio

        seqs = [
            [10**i for i in range(1, 7)],
            [-10**i for i in range(1, 7)],
            [10**(-i) for i in range(1, 10)],
            [-10**(-i) for i in range(1, 10)],
        ]
        
        # 1. Numerical check for unbounded derivative
        for seq in seqs:
            slopes = []
            for p in seq:
                if not is_in_domain(p):
                    continue
                try:
                    step = abs(p) * 1e-3 if p != 0 else 1e-6
                    if step == 0: step = 1e-6
                    if step > 1e-3: step = 1e-3
                    
                    v1 = g(p)
                    v2 = g(p + step)
                    slopes.append(abs(v2 - v1) / step)
                except Exception:
                    pass
            if is_unbounded(slopes):
                neg_q = True
                break

        # 2. Fallback to symbolic limits of the derivative
        if not neg_q:
            try:
                for f in F:
                    df = sympy.diff(f, x)
                    for limit_pt in [sympy.oo, -sympy.oo, 0]:
                        try:
                            if limit_pt == sympy.oo:
                                if getattr(domain, 'sup', None) != sympy.oo and domain != sympy.S.Reals:
                                    continue
                            elif limit_pt == -sympy.oo:
                                if getattr(domain, 'inf', None) != -sympy.oo and domain != sympy.S.Reals:
                                    continue
                            elif limit_pt == 0:
                                if domain != sympy.S.Reals:
                                    try:
                                        if not domain.closure.contains(0):
                                            continue
                                    except Exception:
                                        pass
                                        
                            lim = sympy.limit(df, x, limit_pt)
                            if lim.is_infinite:
                                neg_q = True
                                break
                            if hasattr(lim, 'max') and lim.max == sympy.oo:
                                neg_q = True
                                break
                            if hasattr(lim, 'min') and lim.min == -sympy.oo:
                                neg_q = True
                                break
                        except Exception:
                            pass
            except Exception:
                pass
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a family of functions from a metric space (X, d) to the real numbers",
    "H_2: There exists at least one point x_0 in X such that the infimum over f in F of f(x_0) is a finite real number",
    "¬Q: The pointwise infimum function g(x) = \\inf_{f \\in F} f(x) is NOT L-Lipschitz continuous on X"
]
N_HYP = 2
NEG_Q_INDEX = 2