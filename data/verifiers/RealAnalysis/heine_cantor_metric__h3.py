import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: Y is a metric space",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # The witness is expected to be a tuple (X, f)
        # where X is a sympy.Set representing the domain
        # and f is a sympy.Expr representing the function f: X -> Y
        X, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: X is a compact metric space
    try:
        h1 = False
        if isinstance(X, sympy.Set) and X.is_subset(sympy.S.Reals):
            # In R^n, compact is equivalent to closed and bounded (Heine-Borel)
            if X.is_bounded:
                if getattr(X, 'is_closed', None) is True:
                    h1 = True
                elif X.closure == X:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: Y is a metric space
    try:
        h2 = False
        if isinstance(f, sympy.Expr) and f.free_symbols.issubset({x}):
            # Check if f evaluates to a real number (thus Y is a subset of Reals, a metric space)
            if not X.is_empty:
                pt = None
                if X.inf in X:
                    pt = X.inf
                elif X.sup in X:
                    pt = X.sup
                else:
                    try:
                        pt = (X.inf + X.sup) / 2
                    except Exception:
                        pass
                
                if pt is not None:
                    val = f.subs(x, pt)
                    if val.is_real:
                        h2 = True
                    elif val.is_number:
                        try:
                            # Check for finite real number (excludes zoo, nan, complex)
                            if float(val) == float(val):
                                h2 = True
                        except Exception:
                            pass
                else:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: f is not uniformly continuous on X
    try:
        neg_q = False
        if isinstance(X, sympy.FiniteSet):
            # Any function on a finite metric space is uniformly continuous
            neg_q = False
        else:
            # Try using sympy's continuous_domain
            try:
                from sympy.calculus.util import continuous_domain
                cd = continuous_domain(f, x, X)
                is_sub = X.is_subset(cd)
                if is_sub is False:
                    neg_q = True
            except Exception:
                pass
            
            # Try using sympy's singularities
            if not neg_q:
                try:
                    from sympy.calculus.singularities import singularities
                    sings = singularities(f, x)
                    if isinstance(sings, sympy.Set):
                        intersect = X.intersect(sings)
                        if not intersect.is_empty:
                            neg_q = True
                except Exception:
                    pass

            # Fallback for Piecewise functions (checking boundary limits)
            if not neg_q:
                for pw in f.atoms(sympy.Piecewise):
                    for expr, cond in pw.args:
                        if isinstance(cond, (sympy.StrictLessThan, sympy.LessThan, sympy.StrictGreaterThan, sympy.GreaterThan, sympy.Eq)):
                            for arg in cond.args:
                                if arg != x and arg.is_number:
                                    c = arg
                                    if X.contains(c) == True:
                                        left_lim = sympy.limit(f, x, c, dir='-')
                                        right_lim = sympy.limit(f, x, c, dir='+')
                                        val = f.subs(x, c)
                                        if not (left_lim == right_lim == val):
                                            neg_q = True
                                            break
                        if neg_q:
                            break
                    if neg_q:
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]