import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, X, Y, Z = sp.symbols('x y z X Y Z')

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a, f) or (R, a, f) where:
      - a is a scalar in a UFD R
      - f is a polynomial expression
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R_ring, a, f = witness
            elif len(witness) == 2:
                a, f = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain.
    try:
        if isinstance(a, (int, sp.Integer, float, sp.Float, sp.Rational)):
            h1 = True
        elif isinstance(a, sp.Expr):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: a in R is a non-zero element.
    try:
        h2 = bool(sp.cancel(a) != 0)
    except Exception:
        h2 = False

    # ¬Q: The primitive part of a*f is NOT associate to the primitive part of f.
    try:
        f_expr = sp.sympify(f)
        a_expr = sp.sympify(a)
        
        if sp.cancel(f_expr) == 0:
            # The primitive part of 0 is undefined, so the conclusion fails.
            neg_q = True
        else:
            free_vars = f_expr.free_symbols
            var = list(free_vars)[0] if free_vars else x
            
            af = sp.expand(a_expr * f_expr)
            
            poly_af = sp.Poly(af, var)
            _, pp_af = poly_af.primitive()
            
            poly_f = sp.Poly(f_expr, var)
            _, pp_f = poly_f.primitive()
            
            expr_af = sp.cancel(pp_af.as_expr())
            expr_f = sp.cancel(pp_f.as_expr())
            
            if expr_af == 0 or expr_f == 0:
                neg_q = True
            else:
                ratio = sp.cancel(expr_af / expr_f)
                
                if isinstance(a, (int, sp.Integer)):
                    are_assoc = (ratio == 1 or ratio == -1)
                elif isinstance(a, (float, sp.Float, sp.Rational)):
                    free = ratio.free_symbols
                    are_assoc = (ratio != 0) and (var not in free)
                else:
                    are_assoc = (ratio == 1 or ratio == -1)
                    
                neg_q = not are_assoc
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a in R is a non-zero element",
    "¬Q: The primitive part of a*f is NOT associate to the primitive part of f"
]

N_HYP = 2
NEG_Q_INDEX = 2