import sympy
from sympy import Symbol, S, Interval, FiniteSet, oo
from sympy.calculus.util import function_range

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture:
    "If (X, d_X) and (Y, d_Y) are metric spaces and A is a totally bounded set in X, 
    then f(A) is a totally bounded set in Y."
    
    The witness should provide a set A and a function f.
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            f = witness.get('f')
            x_sym = witness.get('x', x)
        elif isinstance(witness, (list, tuple)):
            A = witness[0]
            f = witness[1]
            x_sym = witness[2] if len(witness) > 2 else x
        else:
            return [False, False, False]
            
        if A is None or f is None:
            return [False, False, False]
            
        if callable(f):
            f = f(x_sym)
    except Exception:
        return [False, False, False]

    # H_1: (X, d_X) and (Y, d_Y) are metric spaces
    # We assume the context is the real line with the standard metric.
    try:
        h1 = bool(A.is_subset(S.Reals))
    except Exception:
        h1 = False

    # H_2: A is a totally bounded set
    # In R^n, totally bounded is equivalent to bounded.
    try:
        h2 = False
        if hasattr(A, 'is_bounded') and A.is_bounded is not None:
            h2 = bool(A.is_bounded)
        elif hasattr(A, 'inf') and hasattr(A, 'sup'):
            h2 = bool(A.inf.is_finite and A.sup.is_finite)
    except Exception:
        h2 = False

    # ¬Q: f(A) is not a totally bounded set
    try:
        neg_q = False
        if getattr(A, 'is_FiniteSet', False):
            image_vals = [f.subs(x_sym, val) for val in A]
            neg_q = not all(v.is_finite for v in image_vals)
        else:
            image = function_range(f, x_sym, A)
            is_real_valued = image.is_subset(S.Reals)
            # Ensure the function is well-defined and real-valued on A
            if is_real_valued is not False:
                if hasattr(image, 'is_bounded') and image.is_bounded is not None:
                    neg_q = not bool(image.is_bounded)
                elif hasattr(image, 'inf') and hasattr(image, 'sup'):
                    neg_q = not bool(image.inf.is_finite and image.sup.is_finite)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces (assumed R)",
    "H_2: A is a totally bounded set",
    "¬Q: f(A) is not a totally bounded set"
]

N_HYP = 2
NEG_Q_INDEX = 2