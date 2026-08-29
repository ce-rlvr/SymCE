import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (B, f) where:
      - B is a sympy.Set (e.g., sympy.S.Reals, sympy.Interval.open(0, 1))
      - f is a sympy.Lambda or sympy.Expr representing the function f(x)
    """
    try:
        B, f = witness
        if isinstance(f, sympy.Lambda):
            if len(f.variables) != 1:
                return [False, False]
            var = f.variables[0]
            expr = f.expr
        elif isinstance(f, sympy.Expr):
            free_vars = list(f.free_symbols)
            if len(free_vars) == 1:
                var = free_vars[0]
            elif len(free_vars) == 0:
                var = sympy.Symbol('x', real=True)
            else:
                return [False, False]
            expr = f
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: f: B -> B is a continuous function
    try:
        if B.is_empty:
            h1 = False
        elif not (B.is_subset(sympy.S.Reals) == True):
            h1 = False
        else:
            # Check continuity on B
            cd = sympy.continuous_domain(expr, var, sympy.S.Reals)
            is_cont = (B.is_subset(cd) == True)
            
            # Check f(B) is a subset of B
            is_into = False
            try:
                image = sympy.function_range(expr, var, B)
                is_into = (image.is_subset(B) == True)
            except Exception:
                pass
                
            if not is_into:
                try:
                    img_set = sympy.imageset(var, B, expr)
                    is_into = (img_set.is_subset(B) == True)
                except Exception:
                    pass
                
            h1 = is_cont and is_into
    except Exception:
        h1 = False

    # neg_Q: There is NO point x in B such that f(x) = x
    try:
        fixed_points = sympy.solveset(expr - var, var, domain=B)
        neg_q = (fixed_points.is_empty == True)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f: B -> B is a continuous function",
    "¬Q: There is no point x in B such that f(x) = x"
]

N_HYP = 1
NEG_Q_INDEX = 1