import sympy as sp
from sympy.abc import x, n

# Top-level setup
# We define x and n as symbols that might be used in the witness expressions.
# The verifier will internally replace them with properly assumed symbols.

def get_sample_points(domain, num_points=20):
    points = set()
    try:
        if hasattr(domain, 'is_Interval') and domain.is_Interval:
            inf = domain.inf
            sup = domain.sup
            if inf == -sp.oo and sup == sp.oo:
                bounds = [-10.0, 10.0]
            elif inf == -sp.oo:
                bounds = [float(sup) - 20.0, float(sup)]
            elif sup == sp.oo:
                bounds = [float(inf), float(inf) + 20.0]
            else:
                bounds = [float(inf), float(sup)]
            
            w = bounds[1] - bounds[0]
            for i in range(num_points):
                pt = bounds[0] + w * (i + 0.5) / num_points
                points.add(pt)
                
            if not domain.left_open and inf != -sp.oo:
                points.add(float(inf))
            if not domain.right_open and sup != sp.oo:
                points.add(float(sup))
        elif isinstance(domain, sp.FiniteSet):
            points = set(float(p) for p in domain)
        elif hasattr(domain, 'args') and domain.args:
            for arg in domain.args:
                points.update(get_sample_points(arg, max(1, num_points // len(domain.args))))
    except Exception:
        pass
    if not points:
        points = {0.0, 1.0, 2.0, -1.0, 0.5}
    return list(points)

def check_H1(f_n, x_sym, n_sym, domain):
    for n_val in [1, 2, 3]:
        try:
            fn_sub = f_n.subs(n_sym, n_val)
            cd = sp.calculus.util.continuous_domain(fn_sub, x_sym, sp.S.Reals)
            if not domain.is_subset(cd):
                return False
        except Exception:
            return False
    return True

def check_H2(f_n, x_sym, n_sym, domain):
    diff_n = f_n - f_n.subs(n_sym, n_sym + 1)
    try:
        for n_val in [1, 2, 5]:
            diff_sub = diff_n.subs(n_sym, n_val)
            min_val = sp.minimum(diff_sub, x_sym, domain)
            if min_val < 0:
                return False
        return True
    except Exception:
        pass
        
    pts = get_sample_points(domain, 100)
    for n_val in [1, 2, 5, 10]:
        diff_sub = diff_n.subs(n_sym, n_val)
        for pt in pts:
            try:
                val = float(diff_sub.subs(x_sym, pt))
                if val < -1e-7:
                    return False
            except Exception:
                pass
    return True

def check_H3(f_n, f, x_sym, n_sym, domain):
    try:
        cd = sp.calculus.util.continuous_domain(f, x_sym, sp.S.Reals)
        if not domain.is_subset(cd):
            return False
    except Exception:
        pass
        
    try:
        lim_f = sp.limit(f_n, n_sym, sp.oo)
        diff = lim_f - f
        if diff == 0:
            return True
            
        pts = get_sample_points(domain, 20)
        all_match = True
        for pt in pts:
            try:
                val = float(diff.subs(x_sym, pt))
                if abs(val) > 1e-7:
                    all_match = False
                    break
            except Exception:
                pass
        if all_match:
            return True
    except Exception:
        pass
        
    pts = get_sample_points(domain, 50)
    for pt in pts:
        try:
            f_val = float(f.subs(x_sym, pt))
            fn_val = float(f_n.subs({n_sym: 1000, x_sym: pt}))
            if abs(fn_val - f_val) > 1e-2:
                fn_val2 = float(f_n.subs({n_sym: 10000, x_sym: pt}))
                if abs(fn_val2 - f_val) >= abs(fn_val - f_val) - 1e-5:
                    return False
        except Exception:
            pass
            
    return True

def check_neg_Q(f_n, f, x_sym, n_sym, domain):
    diff = sp.Abs(f_n - f)
    try:
        sup_n = sp.maximum(diff, x_sym, domain)
        lim = sp.limit(sup_n, n_sym, sp.oo)
        if lim == 0:
            return False
        else:
            return True
    except Exception:
        pass
        
    try:
        max_diffs = []
        for n_val in [10, 100, 1000]:
            expr = f_n.subs(n_sym, n_val) - f
            try:
                m1 = sp.maximum(expr, x_sym, domain)
                m2 = sp.maximum(-expr, x_sym, domain)
                m = max(float(m1), float(m2))
                max_diffs.append(m)
            except Exception:
                deriv = sp.diff(expr, x_sym)
                crit_pts = sp.solveset(deriv, x_sym, domain=domain)
                pts_to_check = set()
                if isinstance(crit_pts, sp.FiniteSet):
                    pts_to_check.update(crit_pts)
                if hasattr(domain, 'is_Interval') and domain.is_Interval:
                    if domain.inf != -sp.oo: pts_to_check.add(domain.inf)
                    if domain.sup != sp.oo: pts_to_check.add(domain.sup)
                pts_to_check.update(get_sample_points(domain, 20))
                
                m = 0
                for pt in pts_to_check:
                    try:
                        val = abs(float(expr.subs(x_sym, pt)))
                        if val > m: m = val
                    except Exception:
                        try:
                            val = abs(float(sp.limit(expr, x_sym, pt)))
                            if val > m: m = val
                        except Exception:
                            pass
                max_diffs.append(m)
                
        if len(max_diffs) >= 2:
            if max_diffs[-1] > 1e-3:
                return True
            else:
                return False
    except Exception:
        pass
        
    return False

def conditions(witness):
    if isinstance(witness, dict):
        domain = witness.get('domain')
        f_n = witness.get('f_n')
        f = witness.get('f')
    else:
        domain, f_n, f = witness

    f_n = sp.sympify(f_n)
    f = sp.sympify(f)

    free_syms = set()
    if hasattr(f_n, 'free_symbols'):
        free_syms.update(f_n.free_symbols)
    if hasattr(f, 'free_symbols'):
        free_syms.update(f.free_symbols)
        
    x_sym = next((s for s in free_syms if s.name == 'x'), x)
    n_sym = next((s for s in free_syms if s.name == 'n'), n)
    
    x_real = sp.Symbol(x_sym.name, real=True)
    n_pos = sp.Symbol(n_sym.name, integer=True, positive=True)
    
    if hasattr(f_n, 'subs'):
        f_n = f_n.subs({x_sym: x_real, n_sym: n_pos})
    if hasattr(f, 'subs'):
        f = f.subs({x_sym: x_real, n_sym: n_pos})

    h1_ok = False
    try:
        h1_ok = check_H1(f_n, x_real, n_pos, domain)
    except Exception:
        pass

    h2_ok = False
    try:
        h2_ok = check_H2(f_n, x_real, n_pos, domain)
    except Exception:
        pass

    h3_ok = False
    try:
        h3_ok = check_H3(f_n, f, x_real, n_pos, domain)
    except Exception:
        pass

    neg_q_ok = False
    try:
        neg_q_ok = check_neg_Q(f_n, f, x_real, n_pos, domain)
    except Exception:
        pass

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of continuous real-valued functions on X",
    "H_2: For each x in X, (f_n(x)) is monotonically decreasing",
    "H_3: (f_n) converges pointwise to a continuous function f on X",
    "¬Q: (f_n) does not converge uniformly to f on X"
]

N_HYP = 3
NEG_Q_INDEX = 3