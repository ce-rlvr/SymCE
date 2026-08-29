import sympy
from sympy import Symbol, FiniteSet, Interval, Union, S, limit, Limit, sympify
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def is_compact(K):
    if isinstance(K, FiniteSet):
        return all(e.is_real and e.is_finite for e in K.args)
    if isinstance(K, Interval):
        return (not K.left_open) and (not K.right_open) and K.start.is_finite and K.end.is_finite
    if isinstance(K, Union):
        return all(is_compact(arg) for arg in K.args)
    
    try:
        if not K.is_subset(S.Reals):
            return False
        if not K.is_closed:
            return False
        if K.inf.is_infinite or K.sup.is_infinite:
            return False
        return True
    except Exception:
        return False

def is_continuous_on_K(f, x_sym, K):
    if isinstance(K, FiniteSet):
        return True
    
    components = K.args if isinstance(K, Union) else [K]
    
    cd = continuous_domain(f, x_sym, S.Reals)
    
    for comp in components:
        if isinstance(comp, FiniteSet):
            continue
        elif isinstance(comp, Interval):
            a = comp.start
            b = comp.end
            interior = Interval(a, b, True, True)
            if not interior.is_subset(cd):
                return False
            if not comp.left_open:
                lim_a = limit(f, x_sym, a, dir='+')
                if isinstance(lim_a, Limit) or lim_a != f.subs(x_sym, a):
                    return False
            if not comp.right_open:
                lim_b = limit(f, x_sym, b, dir='-')
                if isinstance(lim_b, Limit) or lim_b != f.subs(x_sym, b):
                    return False
        else:
            if not comp.is_subset(cd):
                return False
                
    return True

def conditions(witness) -> list[bool]:
    try:
        K, f = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_compact(K)
    except Exception:
        h1 = False
        
    try:
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = sympify(f, locals={'x': x})
            
        f_continuous = is_continuous_on_K(f_expr, x, K)
        neg_q = not f_continuous
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a compact subset of R^n",
    "¬Q: There does not exist a continuous function F: R^n -> R extending f"
]

N_HYP = 1
NEG_Q_INDEX = 1