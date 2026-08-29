import sympy
from sympy import Poly, QQ, sqrt, Expr
from sympy.abc import x

f_target = x**4 - 2*x**3 + x**2 - 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either the field K, or a tuple (f(x), K).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        f_val, K_val = witness
    else:
        f_val = witness
        K_val = witness

    # H_1: f(x) = x^4 - 2x^3 + x^2 - 1 in QQ
    h1 = False
    try:
        if f_val == f_target:
            h1 = True
        elif hasattr(f_val, 'as_expr') and sympy.simplify(f_val.as_expr() - f_target) == 0:
            h1 = True
        elif isinstance(f_val, Expr) and sympy.simplify(f_val - f_target) == 0:
            h1 = True
        elif not (isinstance(witness, tuple) and len(witness) == 2):
            # If witness is just K, f(x) is implicitly f_target, so the hypothesis holds vacuously.
            h1 = True
    except Exception:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            h1 = True

    # Conclusion: K = QQ(sqrt(5), sqrt(-3)) and [K:QQ] = 4
    q = False
    try:
        K_target1 = QQ.algebraic_field(sqrt(5), sqrt(-3))
        K_target2 = QQ.algebraic_field(sqrt(-3), sqrt(5))
        
        if K_val == K_target1 or K_val == K_target2:
            q = True
        elif isinstance(K_val, (list, tuple, set)):
            try:
                K_gen = QQ.algebraic_field(*K_val)
                if K_gen == K_target1 or K_gen == K_target2:
                    q = True
            except Exception:
                pass
        
        if not q:
            from sympy import minpoly
            mp_target = minpoly(sqrt(5) + sqrt(-3), x)
            
            gen = None
            if isinstance(K_val, (list, tuple, set)) and len(K_val) == 1:
                gen = list(K_val)[0]
            elif isinstance(K_val, Expr):
                gen = K_val
            
            if gen is not None:
                mp = minpoly(gen, x)
                if mp == mp_target:
                    q = True
            elif hasattr(K_val, 'ext') and hasattr(K_val.ext, 'minpoly'):
                try:
                    mod_expr = K_val.ext.minpoly.as_expr()
                    mod_gen = K_val.ext.minpoly.gen
                    if sympy.simplify(mod_expr.subs(mod_gen, x) - mp_target) == 0:
                        q = True
                except Exception:
                    pass
    except Exception:
        q = False

    neg_q = not q
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = x^4 - 2x^3 + x^2 - 1 in QQ",
    "¬Q: K is not Q(sqrt(5), sqrt(-3)) or degree is not 4"
]

N_HYP = 1
NEG_Q_INDEX = 1