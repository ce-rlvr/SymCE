import sympy
from sympy import Symbol

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide both the function f and the family F,
    since the hypothesis defining F was dropped.
    """
    try:
        # Extract f and F from the witness
        if isinstance(witness, dict):
            f = witness.get('f')
            F = witness.get('F')
        elif isinstance(witness, tuple) and len(witness) == 2:
            f, F = witness
        else:
            f = getattr(witness, 'f', None)
            F = getattr(witness, 'F', None)
            
        if f is None or F is None:
            return [False, False]
            
        # Parse strings if necessary
        if isinstance(f, str):
            f = sympy.sympify(f)
        if isinstance(F, str):
            F = sympy.sympify(F)
        elif isinstance(F, list) and len(F) > 0 and isinstance(F[0], str):
            F = [sympy.sympify(g) for g in F]
            
    except Exception:
        return [False, False]

    # H_1: f is a continuous function on R
    try:
        if hasattr(f, 'free_symbols'):
            syms = list(f.free_symbols)
            var = syms[0] if syms else x
            dom = sympy.calculus.util.continuous_domain(f, var, sympy.S.Reals)
            h1 = (dom == sympy.S.Reals)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: f is uniformly continuous on R iff the family F is uniformly equicontinuous on R is FALSE
    try:
        def is_uc(expr, var):
            """Heuristic to check if a sympy expression is uniformly continuous on R."""
            try:
                dom = sympy.calculus.util.continuous_domain(expr, var, sympy.S.Reals)
                if dom != sympy.S.Reals:
                    return False
            except Exception:
                pass
            
            if expr.is_polynomial(var):
                return sympy.degree(expr, var) <= 1
                
            df = sympy.diff(expr, var)
            if df.is_zero:
                return True
                
            try:
                l1 = sympy.limit(df, var, sympy.oo)
                l2 = sympy.limit(df, var, -sympy.oo)
                if l1.is_finite == True and l2.is_finite == True:
                    return True
            except Exception:
                pass
                
            return False

        def is_uec(family, var):
            """Heuristic to check if a family of functions is uniformly equicontinuous."""
            if isinstance(family, (list, tuple, set)):
                if not family:
                    return True
                return all(is_uc(g, var) for g in family)
            return is_uc(family, var)

        # Evaluate uniform continuity of f
        if hasattr(f, 'free_symbols'):
            syms = list(f.free_symbols)
            var_f = syms[0] if syms else x
            uc_f = is_uc(f, var_f)
        else:
            uc_f = False

        # Evaluate uniform equicontinuity of F
        if isinstance(F, (list, tuple, set)):
            if len(F) > 0:
                first = list(F)[0]
                if hasattr(first, 'free_symbols'):
                    syms = list(first.free_symbols)
                    var_F = syms[0] if syms else x
                else:
                    var_F = x
            else:
                var_F = x
            uec_F = is_uec(F, var_F)
        else:
            if hasattr(F, 'free_symbols'):
                syms = list(F.free_symbols)
                var_F = syms[0] if syms else x
            else:
                var_F = x
            uec_F = is_uec(F, var_F)

        # The biconditional is false if the truth values differ
        neg_q = (uc_f != uec_F)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuous function on R",
    "¬Q: f is uniformly continuous on R iff the family F is uniformly equicontinuous on R is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1