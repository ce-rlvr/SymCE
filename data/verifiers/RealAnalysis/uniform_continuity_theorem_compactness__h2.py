import sympy
from sympy import Symbol, S, Interval, Union, FiniteSet, oo, limit
from sympy.calculus.util import continuous_domain

# Top-level setup: named object bindings for the witness expression
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

def is_compact(domain):
    try:
        if domain.is_Interval:
            return (not domain.left_open) and (not domain.right_open) and domain.start.is_finite and domain.end.is_finite
        if isinstance(domain, Union):
            return all(is_compact(arg) for arg in domain.args)
        if isinstance(domain, FiniteSet):
            return True
        if domain == S.EmptySet:
            return True
        return False
    except Exception:
        return False

def is_continuous(f, domain, sym):
    try:
        cd = continuous_domain(f, sym, S.Reals)
        res = domain.is_subset(cd)
        return bool(res) if res is not None else False
    except Exception:
        return False

def is_convergent_and_finite(L):
    if L.has(sympy.AccumBounds):
        return False
    return L.is_finite

def is_bounded_limit(L):
    if isinstance(L, sympy.AccumBounds):
        return L.min.is_finite and L.max.is_finite
    if L.has(sympy.AccumBounds):
        for arg in L.atoms(sympy.AccumBounds):
            if not arg.min.is_finite or not arg.max.is_finite:
                return False
        return True
    return L.is_finite

def is_uniformly_continuous(f, domain, sym):
    try:
        if not is_continuous(f, domain, sym):
            return False
            
        if is_compact(domain):
            return True
            
        if domain.is_Interval:
            a, b = domain.start, domain.end
            
            if a.is_finite:
                L_a = limit(f, sym, a, dir='+')
                if not is_convergent_and_finite(L_a):
                    return False
            else:
                df = f.diff(sym)
                L_df = limit(df, sym, -oo)
                if not is_bounded_limit(L_df):
                    return False
                    
            if b.is_finite:
                L_b = limit(f, sym, b, dir='-')
                if not is_convergent_and_finite(L_b):
                    return False
            else:
                df = f.diff(sym)
                L_df = limit(df, sym, oo)
                if not is_bounded_limit(L_df):
                    return False
                    
            return True
            
        if isinstance(domain, Union):
            return all(is_uniformly_continuous(f, arg, sym) for arg in domain.args)
            
        if isinstance(domain, FiniteSet):
            return True
            
        return True
    except Exception:
        return True

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (domain, f) where domain is a SymPy Set and f is a SymPy Expr.
    Alternatively, it can just be a SymPy Expr f, with the domain implicitly being S.Reals.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, f = witness
        else:
            domain = S.Reals
            f = witness
            
        f = sympy.sympify(f)
        free_symbols = f.free_symbols
        if len(free_symbols) == 1:
            sym = list(free_symbols)[0]
        else:
            sym = x
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(is_compact(domain))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_continuous(f, domain, sym))
    except Exception:
        h2 = False

    try:
        neg_q = not is_uniformly_continuous(f, domain, sym)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: f is continuous on X",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2