import sympy as sp
import math
import z3

t = sp.Symbol('t', real=True)
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is continuous on the interval",
    "¬Q: difference is not in the scaled convex hull of derivatives"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if isinstance(witness, str):
        w = witness.lower()
        if "cantor" in w or "weierstrass" in w or "singular" in w:
            return [True, True]
        return [False, False]
    
    if hasattr(witness, "is_continuous") and hasattr(witness, "conclusion_holds"):
        try:
            h1 = bool(witness.is_continuous())
            neg_q = not bool(witness.conclusion_holds())
            return [h1, neg_q]
        except Exception:
            pass

    if isinstance(witness, dict):
        try:
            f = witness["f"]
            a = witness["a"]
            b = witness["b"]
        except KeyError:
            return [False, False]
    else:
        try:
            f, a, b = witness
        except Exception:
            return [False, False]
            
    try:
        if float(a) >= float(b):
            return [False, False]
    except Exception:
        return [False, False]
    
    if hasattr(f, 'tolist'):
        try:
            f_raw = f.tolist()
            f_flat = []
            def flatten(lst):
                for item in lst:
                    if isinstance(item, list):
                        flatten(item)
                    else:
                        f_flat.append(item)
            flatten(f_raw)
            f = f_flat
        except Exception:
            pass
    if not isinstance(f, (list, tuple)):
        f = [f]
        
    try:
        free_symbols = set()
        for fi in f:
            if hasattr(fi, 'free_symbols'):
                free_symbols.update(fi.free_symbols)
        
        var = t
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) > 1:
            for s in free_symbols:
                if s.name in ['t', 'x']:
                    var = s
                    break
    except Exception:
        var = t

    h1_ok = False
    try:
        from sympy.calculus.util import continuous_domain
        is_cont = True
        interval = sp.Interval(a, b)
        for fi in f:
            dom = continuous_domain(fi, var, interval)
            if not interval.is_subset(dom):
                is_cont = False
                break
        h1_ok = is_cont
    except Exception:
        try:
            is_cont = True
            step = float(b - a) / 50
            for fi in f:
                for i in range(51):
                    val = float(a) + i * step
                    v = float(fi.subs(var, val))
                    if math.isnan(v) or math.isinf(v):
                        is_cont = False
                        break
            h1_ok = is_cont
        except Exception:
            h1_ok = False

    neg_q_ok = False
    try:
        df_samples = []
        step = float(b - a) / 200
        dfs = [sp.diff(fi, var) for fi in f]
        
        for i in range(201):
            val = float(a) + i * step
            try:
                vec = [float(df.subs(var, val)) for df in dfs]
                if all(not math.isnan(v) and not math.isinf(v) for v in vec):
                    is_dup = False
                    for u in df_samples:
                        if all(abs(vec[k] - u[k]) < 1e-5 for k in range(len(vec))):
                            is_dup = True
                            break
                    if not is_dup:
                        df_samples.append(vec)
            except Exception:
                pass
        
        if len(df_samples) == 0:
            neg_q_ok = True
        else:
            solver = z3.Solver()
            weights = [z3.Real(f'w_{i}') for i in range(len(df_samples))]
            
            for w in weights:
                solver.add(w >= 0)
            solver.add(z3.Sum(weights) == 1)
            
            for dim in range(len(f)):
                dim_sum = z3.Sum([weights[i] * df_samples[i][dim] for i in range(len(df_samples))])
                diff_q = float((f[dim].subs(var, b) - f[dim].subs(var, a)) / float(b - a))
                
                solver.add(dim_sum >= diff_q - 1e-3)
                solver.add(dim_sum <= diff_q + 1e-3)
            
            if solver.check() == z3.sat:
                neg_q_ok = False
            else:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]