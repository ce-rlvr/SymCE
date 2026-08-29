import sympy
from sympy import Symbol, S, limit, oo, Abs, diff, solve, pi
import math
import itertools
import functools

# Top-level setup
# No specific named objects required for this real analysis theorem.

def is_bounded(f_expr, x):
    try:
        from sympy.calculus.util import function_range
        fr = function_range(f_expr, x, S.Reals)
        if fr.inf == -oo or fr.sup == oo:
            return False
        return True
    except Exception:
        pass
    
    try:
        L1 = limit(f_expr, x, oo)
        L2 = limit(f_expr, x, -oo)
        if L1 in [oo, -oo] or L2 in [oo, -oo]:
            return False
        
        for val in [-100, -10, -1, 0, 1, 10, 100]:
            if Abs(f_expr.subs(x, val)) == oo:
                return False
                
        sings = sympy.calculus.singularities(f_expr, x)
        for s in sings:
            if s.is_real:
                return False
                
        return True
    except Exception:
        # Fallback heuristic evaluation
        import random
        for _ in range(20):
            try:
                val = f_expr.subs(x, random.uniform(-100, 100))
                if abs(float(val)) > 1e6:
                    return False
            except Exception:
                pass
        return True

def converges_uniformly_to_zero(f_n_expr, x, n):
    try:
        L1 = limit(f_n_expr, x, oo)
        if L1 != 0:
            lim1 = limit(Abs(L1), n, oo)
            if lim1 != 0 and getattr(lim1, 'is_zero', None) is not True:
                return False
    except Exception:
        pass

    try:
        L2 = limit(f_n_expr, x, -oo)
        if L2 != 0:
            lim2 = limit(Abs(L2), n, oo)
            if lim2 != 0 and getattr(lim2, 'is_zero', None) is not True:
                return False
    except Exception:
        pass

    try:
        df = diff(f_n_expr, x)
        cps = solve(df, x)
        for cp in cps:
            if cp.has(sympy.I):
                continue
            val = f_n_expr.subs(x, cp)
            lim_val = limit(Abs(val), n, oo)
            if lim_val != 0 and getattr(lim_val, 'is_zero', None) is not True:
                return False
    except Exception:
        pass

    try:
        for seq in [n, 1/n, n**2, S(1), S(0), pi*n, pi*n/2]:
            val = f_n_expr.subs(x, seq)
            lim_seq = limit(Abs(val), n, oo)
            if lim_seq != 0 and getattr(lim_seq, 'is_zero', None) is not True:
                return False
    except Exception:
        pass

    return True

def neg_q_ok(witness, x, n):
    f_n = None
    if isinstance(witness, tuple) and len(witness) == 2:
        f, f_n = witness
    elif isinstance(witness, dict) and 'f_n' in witness:
        f_n = witness['f_n']
    elif hasattr(witness, 'f_n'):
        f_n = witness.f_n
        
    if f_n is not None:
        return not converges_uniformly_to_zero(f_n, x, n)
        
    if isinstance(witness, dict) and 'f' in witness:
        f = witness['f']
    elif hasattr(witness, 'f'):
        f = witness.f
    else:
        f = witness
        
    try:
        if sympy.simplify(f) == 0:
            return False
    except Exception:
        pass
        
    # If f_n is not explicitly provided, we test common scaled sequences 
    # that fail to converge uniformly when a hypothesis is dropped.
    seqs = [
        f.subs(x, n*x),
        f.subs(x, x/n),
        (x/n) * f,
        f / (1 + n * x**2)
    ]
    
    for sq in seqs:
        if not converges_uniformly_to_zero(sq, x, n):
            return True
            
    return False

def conditions(witness):
    x = Symbol('x', real=True)
    n = Symbol('n', integer=True, positive=True)
    
    if isinstance(witness, tuple) and len(witness) == 2:
        f = witness[0]
    elif isinstance(witness, dict) and 'f' in witness:
        f = witness['f']
    elif hasattr(witness, 'f'):
        f = witness.f
    else:
        f = witness
        
    try:
        h1_ok = bool(is_bounded(f, x))
    except Exception:
        h1_ok = False
        
    try:
        neg_q = bool(neg_q_ok(witness, x, n))
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a bounded real-valued function",
    "¬Q: The sequence (f_n) does not converge uniformly to the zero function on R"
]

N_HYP = 1
NEG_Q_INDEX = 1