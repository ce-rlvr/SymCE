import sympy as sp
from sympy import Symbol, S, oo

# Top-level setup for witness expressions
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: X and Y are metric spaces",
    "H_2: f is a function from X to Y",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, f = witness
        else:
            domain = S.Reals
            f = witness
            
        # Handle callable functions
        if callable(f) and not isinstance(f, sp.Expr):
            f = f(x)
            
        # H1: X and Y are metric spaces
        # We assume X is the domain (a subset of Reals) and Y is Reals.
        # Subsets of Reals with the standard metric are metric spaces.
        if isinstance(domain, sp.Set):
            h1 = True
            
        # H2: f is a function from X to Y
        # Check if f is defined everywhere on the domain.
        try:
            sings = sp.singularities(f, x)
            if sings.intersect(domain) == S.EmptySet:
                h2 = True
        except Exception:
            # Fallback if singularities cannot be computed
            if hasattr(f, 'is_polynomial') and f.is_polynomial(x):
                h2 = True
            elif isinstance(f, sp.Expr):
                h2 = True

        # neg_Q: f is NOT uniformly continuous on X
        try:
            if domain.is_Interval or domain == S.Reals:
                # 1. Polynomial of degree >= 2 on an unbounded domain
                if hasattr(f, 'is_polynomial') and f.is_polynomial(x):
                    deg = sp.degree(f, x)
                    if deg >= 2 and (domain.sup == oo or domain.inf == -oo):
                        neg_q = True
                
                # 2. Derivative limit at infinity
                if not neg_q:
                    df = sp.diff(f, x)
                    if domain.sup == oo:
                        L = sp.limit(sp.Abs(df), x, oo)
                        if L == oo:
                            neg_q = True
                    if domain.inf == -oo and not neg_q:
                        L = sp.limit(sp.Abs(df), x, -oo)
                        if L == oo:
                            neg_q = True
                            
                # 3. Boundary limits for open intervals
                if not neg_q and domain.is_Interval:
                    if getattr(domain, 'left_open', False) and domain.inf != -oo:
                        L = sp.limit(f, x, domain.inf, dir='+')
                        if L in [oo, -oo]:
                            neg_q = True
                    if getattr(domain, 'right_open', False) and domain.sup != oo and not neg_q:
                        L = sp.limit(f, x, domain.sup, dir='-')
                        if L in [oo, -oo]:
                            neg_q = True
        except Exception:
            pass

    except Exception:
        pass

    return [h1, h2, neg_q]