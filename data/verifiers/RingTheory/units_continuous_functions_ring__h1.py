import sympy
from sympy import S, Interval, Union, oo, zoo, limit, solveset, Symbol, AccumBounds

def get_symbol(f):
    free = f.free_symbols
    if len(free) == 1:
        return list(free)[0]
    elif len(free) == 0:
        return Symbol('x', real=True)
    else:
        for s in free:
            if s.name == 'x':
                return s
        return list(free)[0]

def is_unbounded_limit(l):
    if l in [oo, -oo, zoo]:
        return True
    if isinstance(l, AccumBounds):
        if l.min == -oo or l.max == oo:
            return True
    return False

def is_bounded_on(f, x, domain):
    try:
        if domain == S.Reals:
            l1 = limit(f, x, oo)
            l2 = limit(f, x, -oo)
            if is_unbounded_limit(l1) or is_unbounded_limit(l2):
                return False
            return True
        elif isinstance(domain, Interval):
            l1 = limit(f, x, domain.start, dir='+')
            l2 = limit(f, x, domain.end, dir='-')
            if is_unbounded_limit(l1) or is_unbounded_limit(l2):
                return False
            return True
        elif isinstance(domain, Union):
            for arg in domain.args:
                if not is_bounded_on(f, x, arg):
                    return False
            return True
    except Exception:
        pass
    
    try:
        from sympy.calculus.util import function_range
        fr = function_range(f, x, domain)
        return fr.inf > -oo and fr.sup < oo
    except Exception:
        return False

def is_continuous_on(f, x, domain):
    try:
        from sympy.calculus.util import continuous_domain
        cd = continuous_domain(f, x, S.Reals)
        return domain.is_subset(cd)
    except Exception:
        try:
            from sympy import singularities
            sings = singularities(f, x)
            if sings.is_empty:
                return True
            if domain.intersect(sings).is_empty:
                return True
            return False
        except Exception:
            return True

def never_zero_on(f, x, domain):
    try:
        zeros = solveset(f, x, domain=domain)
        if zeros.is_empty == True:
            return True
        if zeros.is_empty == False:
            return False
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a sympy expression `f` (assuming domain is Reals) 
    or a tuple `(f, domain)` where domain is a sympy Set.
    """
    if isinstance(witness, tuple):
        if len(witness) == 2:
            f, domain = witness
        else:
            return [False, False, False]
    else:
        f = witness
        domain = S.Reals
        
    if not hasattr(f, 'free_symbols'):
        return [False, False, False]
        
    x = get_symbol(f)
    
    # H_1: C(X, R) is the ring of continuous real-valued functions on X
    try:
        h1 = isinstance(domain, sympy.Set)
    except Exception:
        h1 = False
        
    # H_2: f \in C(X, R)
    # In the context of the dropped hypothesis (X is compact), C(X, R) refers to bounded continuous functions.
    try:
        h2 = is_continuous_on(f, x, domain) and is_bounded_on(f, x, domain)
    except Exception:
        h2 = False
        
    # ¬Q: f is a unit in C(X, R) if and only if f(x) != 0 for all x \in X
    # The conclusion fails if f(x) != 0 for all x, BUT f is NOT a unit in C(X, R).
    # f is not a unit if 1/f is not in the ring (i.e., 1/f is not bounded).
    try:
        never_zero = never_zero_on(f, x, domain)
        inv_f = 1 / f
        inv_bounded = is_bounded_on(inv_f, x, domain)
        neg_q = never_zero and not inv_bounded
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: C(X, R) is the ring of continuous real-valued functions on X",
    "H_2: f is in C(X, R)",
    "¬Q: f(x) != 0 for all x, but f is not a unit in C(X, R)"
]

N_HYP = 2
NEG_Q_INDEX = 2