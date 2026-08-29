import sympy as sp
import itertools

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    def is_diff_nonzero(val1, val2):
        try:
            if hasattr(val1, 'has') and val1.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                return True
            if hasattr(val2, 'has') and val2.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                return True
            diff = (val1 - val2)
            if hasattr(diff, 'evalf'):
                diff = diff.evalf(chop=True)
            if float(abs(diff)) > 1e-9:
                return True
        except Exception:
            try:
                diff_simp = sp.simplify(val1 - val2)
                if diff_simp != 0:
                    return True
            except Exception:
                return False
        return False

    try:
        if isinstance(witness, dict):
            if 'f' not in witness or 'a' not in witness:
                return [False, False, False, False]
            f = witness['f']
            v = witness.get('vars')
            a = witness['a']
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                f, v, a = witness
            elif len(witness) == 2:
                f, a = witness
                v = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        if not isinstance(a, (list, tuple)):
            a = (a,)
        if v is not None and not isinstance(v, (list, tuple)):
            v = (v,)

        if v is None:
            if isinstance(f, sp.Expr):
                v = tuple(sorted(f.free_symbols, key=lambda s: s.name))
            elif isinstance(f, (list, tuple, sp.Matrix)):
                syms = set()
                for fi in f:
                    if isinstance(fi, sp.Expr):
                        syms.update(fi.free_symbols)
                v = tuple(sorted(syms, key=lambda s: s.name))
            else:
                v = ()

        if len(v) < len(a):
            existing_names = {s.name for s in v}
            new_v = list(v)
            for i in range(len(a) - len(v)):
                name = f"dummy_{i}"
                while name in existing_names:
                    name += "_"
                new_sym = sp.Symbol(name)
                new_v.append(new_sym)
                existing_names.add(name)
            v = tuple(new_v)
        elif len(v) > len(a):
            return [False, False, False, False]

        if isinstance(f, (list, tuple, sp.Matrix)):
            is_func = all(isinstance(fi, sp.Expr) for fi in f)
        else:
            is_func = isinstance(f, sp.Expr)
            
        h1 = is_func and isinstance(v, (list, tuple)) and len(v) == len(a)
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False, False]

    try:
        subs_dict = dict(zip(v, a))
        if isinstance(f, (list, tuple, sp.Matrix)):
            fa = [fi.subs(subs_dict).evalf() for fi in f]
            h2 = all(fai.is_real is not False and not (hasattr(fai, 'has') and fai.has(sp.oo, -sp.oo, sp.zoo, sp.nan, sp.I)) for fai in fa)
        else:
            fa = f.subs(subs_dict).evalf()
            h2 = fa.is_real is not False and not (hasattr(fa, 'has') and fa.has(sp.oo, -sp.oo, sp.zoo, sp.nan, sp.I))
    except Exception:
        h2 = False

    if not h2:
        return [h1, False, False, False]

    try:
        h3 = True
        h = sp.Symbol('h', real=True)
        f_list = f if isinstance(f, (list, tuple, sp.Matrix)) else [f]
        
        for fi in f_list:
            fi_a = fi.subs(subs_dict)
            for i, vi in enumerate(v):
                a_h = list(a)
                a_h[i] = a[i] + h
                subs_h = dict(zip(v, a_h))
                fi_h = fi.subs(subs_h)
                dq = (fi_h - fi_a) / h
                lim_plus = sp.limit(dq, h, 0, dir='+')
                lim_minus = sp.limit(dq, h, 0, dir='-')
                
                if isinstance(lim_plus, sp.Limit) or isinstance(lim_minus, sp.Limit):
                    h3 = False
                    break
                
                if (hasattr(lim_plus, 'has') and lim_plus.has(sp.oo, -sp.oo, sp.zoo, sp.nan, sp.I)) or \
                   (hasattr(lim_minus, 'has') and lim_minus.has(sp.oo, -sp.oo, sp.zoo, sp.nan, sp.I)):
                    h3 = False
                    break
                    
                if is_diff_nonzero(lim_plus, lim_minus):
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    try:
        neg_q = False
        t = sp.Symbol('t', real=True)
        f_list = f if isinstance(f, (list, tuple, sp.Matrix)) else [f]
        
        for fi in f_list:
            fi_a = fi.subs(subs_dict)
            
            for d in itertools.product([-2, -1, 0, 1, 2], repeat=len(v)):
                if all(di == 0 for di in d):
                    continue
                path_subs = {vi: a[i] + t * d[i] for i, vi in enumerate(v)}
                fi_t = fi.subs(path_subs)
                lim_plus = sp.limit(fi_t, t, 0, dir='+')
                lim_minus = sp.limit(fi_t, t, 0, dir='-')
                
                if not isinstance(lim_plus, sp.Limit):
                    if is_diff_nonzero(lim_plus, fi_a):
                        neg_q = True
                        break
                if not isinstance(lim_minus, sp.Limit):
                    if is_diff_nonzero(lim_minus, fi_a):
                        neg_q = True
                        break
            if neg_q:
                break
            
            if len(v) == 2 and not neg_q:
                x_sym, y_sym = v
                ax, ay = a
                for power in [2, 3]:
                    for coeff in [1, -1, 2, -2]:
                        path_subs = {y_sym: ay + coeff * (x_sym - ax)**power}
                        fi_t = fi.subs(path_subs)
                        lim_plus = sp.limit(fi_t, x_sym, ax, dir='+')
                        lim_minus = sp.limit(fi_t, x_sym, ax, dir='-')
                        
                        if not isinstance(lim_plus, sp.Limit):
                            if is_diff_nonzero(lim_plus, fi_a):
                                neg_q = True
                                break
                        if not isinstance(lim_minus, sp.Limit):
                            if is_diff_nonzero(lim_minus, fi_a):
                                neg_q = True
                                break
                                
                        path_subs = {x_sym: ax + coeff * (y_sym - ay)**power}
                        fi_t = fi.subs(path_subs)
                        lim_plus = sp.limit(fi_t, y_sym, ay, dir='+')
                        lim_minus = sp.limit(fi_t, y_sym, ay, dir='-')
                        
                        if not isinstance(lim_plus, sp.Limit):
                            if is_diff_nonzero(lim_plus, fi_a):
                                neg_q = True
                                break
                        if not isinstance(lim_minus, sp.Limit):
                            if is_diff_nonzero(lim_minus, fi_a):
                                neg_q = True
                                break
                    if neg_q:
                        break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a function from U to R^m",
    "H_2: a is in U",
    "H_3: f is differentiable at a",
    "¬Q: f is not continuous at a"
]
N_HYP = 3
NEG_Q_INDEX = 3