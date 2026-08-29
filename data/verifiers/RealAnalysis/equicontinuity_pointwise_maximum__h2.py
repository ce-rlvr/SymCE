import math
from sympy import Symbol, Set, S, Max, sympify, Interval, diff, maximum, Abs, lambdify
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

def get_symbol(F, G):
    syms = set()
    for expr in F + G:
        try:
            syms.update(expr.free_symbols)
        except Exception:
            pass
    if len(syms) == 1:
        return list(syms)[0]
    elif len(syms) == 0:
        return Symbol('x', real=True)
    else:
        for s in syms:
            if s.name == 'x':
                return s
        return list(syms)[0]

def is_well_defined(expr, sym, domain):
    try:
        modules = [{'Max': max, 'Min': min}, 'math']
        f_num = lambdify(sym, expr, modules)
        
        if isinstance(domain, Interval) and domain.start.is_finite and domain.end.is_finite:
            start = float(domain.start)
            end = float(domain.end)
            step = (end - start) / 100.0
            points = [start + i * step for i in range(101)]
        else:
            points = [-10.0, -1.0, 0.0, 1.0, 10.0]
            
        for val in points:
            res = f_num(val)
            if isinstance(res, complex) and abs(res.imag) > 1e-9:
                return False
            if math.isnan(res) or math.isinf(res):
                return False
        return True
    except Exception:
        return False

def is_uniformly_continuous(expr, sym, domain):
    expr = sympify(expr)
    if not expr.has(sym):
        return True
        
    is_compact = isinstance(domain, Interval) and not domain.left_open and not domain.right_open and domain.start.is_finite and domain.end.is_finite
    
    if is_compact:
        try:
            if continuous_domain(expr, sym, domain) == domain:
                return True
        except Exception:
            pass
        return False
    else:
        try:
            d = diff(expr, sym)
            if not d.has(sym):
                return True
            max_d = maximum(Abs(d), sym, domain)
            if max_d.is_finite:
                return True
        except Exception:
            pass
        return False

def numerical_is_discontinuous(expr, sym, domain_start, domain_end):
    try:
        modules = [{'Max': max, 'Min': min}, 'math']
        _f = lambdify(sym, expr, modules)
        def f_num(val):
            res = _f(val)
            if isinstance(res, complex):
                if abs(res.imag) > 1e-9:
                    raise ValueError
                return res.real
            return res

        eval_count = [0]
        def check_interval(a, b, depth):
            if eval_count[0] > 2000:
                return False
            eval_count[0] += 1
            
            if depth > 10:
                try:
                    ya = f_num(a)
                    yb = f_num(b)
                    if abs(ya - yb) > 0.05:
                        return True
                except Exception:
                    pass
                return False
                
            step = (b - a) / 10.0
            try:
                prev_y = f_num(a)
            except Exception:
                return False
                
            for i in range(1, 11):
                xi = a + i * step
                try:
                    yi = f_num(xi)
                except Exception:
                    return False
                if abs(yi - prev_y) > 0.05:
                    if check_interval(xi - step, xi, depth + 1):
                        return True
                prev_y = yi
            return False

        return check_interval(float(domain_start), float(domain_end), 0)
    except Exception:
        return False

def is_NOT_uniformly_continuous(expr, sym, domain):
    expr = sympify(expr)
    is_compact = isinstance(domain, Interval) and not domain.left_open and not domain.right_open and domain.start.is_finite and domain.end.is_finite
    
    if is_compact:
        try:
            condom = continuous_domain(expr, sym, domain)
            if condom != domain:
                return True
        except Exception:
            pass
        return numerical_is_discontinuous(expr, sym, domain.start, domain.end)
    else:
        try:
            condom = continuous_domain(expr, sym, domain)
            if condom != domain:
                return True
        except Exception:
            pass
        return False

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        X = witness.get('X')
        F = witness.get('F')
        G = witness.get('G')
        
        if F is None or G is None or X is None:
            return [False, False, False]
            
        if not isinstance(F, (list, tuple, set)):
            F = [F]
        if not isinstance(G, (list, tuple, set)):
            G = [G]
            
        F = [sympify(f) for f in F]
        G = [sympify(g) for g in G]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(X, Set) and X.is_subset(S.Reals)
    except Exception:
        h1 = False
        
    try:
        sym = get_symbol(F, G)
    except Exception:
        sym = Symbol('x', real=True)
        
    try:
        well_defined = True
        for f in F:
            if not is_well_defined(f, sym, X):
                well_defined = False
                break
        for g in G:
            if not is_well_defined(g, sym, X):
                well_defined = False
                break
        if not well_defined:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        if len(G) == 0:
            h2 = False
        else:
            h2 = all(is_uniformly_continuous(g, sym, X) for g in G)
    except Exception:
        h2 = False
        
    try:
        if len(F) == 0 or len(G) == 0:
            neg_q = False
        else:
            H_family = []
            for f in F:
                for g in G:
                    H_family.append(Max(f, g))
            
            neg_q = any(is_NOT_uniformly_continuous(h, sym, X) for h in H_family)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: G is an equicontinuous family of functions from X to R",
    "¬Q: The family H = {max(f, g)} is NOT equicontinuous on X"
]
N_HYP = 2
NEG_Q_INDEX = 2