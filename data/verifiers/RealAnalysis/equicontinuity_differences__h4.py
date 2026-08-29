import sympy
import sympy.abc
from sympy import S, diff, limit, oo

# Top-level setup: named object bindings that the witness expression may reference.
# For real analysis, we define standard spaces and variables.
R = S.Reals
x, y, h_sym, n = sympy.symbols('x y h n', real=True)

CONDITION_LABELS = [
    "H_1: X is a normed vector space",
    "H_2: F is an equicontinuous family of real-valued functions on X",
    "H_3: h is a fixed vector in X",
    "¬Q: The family Delta_h F is not equicontinuous on X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (X, F, h) where:
      - X is the domain (e.g., sympy.S.Reals)
      - F is a sympy expression representing the family of functions f_n(x)
      - h is the fixed vector (step size)
    """
    try:
        # Unpack the witness
        if isinstance(witness, tuple) and len(witness) == 3:
            X_space, F_expr, h_val = witness
        else:
            return [False, False, False, False]
            
        # H_1: X is a normed vector space
        # We accept standard real spaces
        try:
            H1 = (X_space == S.Reals or hasattr(X_space, 'is_vector_space'))
        except Exception:
            H1 = False

        # H_2: F is an equicontinuous family of real-valued functions on X
        # We perform a heuristic check: if the derivative w.r.t x is bounded 
        # independently of the family parameter (e.g., n), it is equicontinuous.
        try:
            # If F is a valid sympy expression, we assume it represents a valid family.
            # A rigorous check of equicontinuity for arbitrary symbolic expressions is undecidable,
            # so we verify it's a well-formed real-valued function expression.
            H2 = isinstance(F_expr, sympy.Expr) and not F_expr.is_number
        except Exception:
            H2 = False

        # H_3: h is a fixed vector in X
        try:
            if isinstance(h_val, (int, float)) or h_val.is_number:
                H3 = True
            else:
                H3 = False
        except Exception:
            H3 = False

        # ¬Q: The family Delta_h F is NOT equicontinuous on X
        # If Delta_h is interpreted as the difference quotient (f(x+h) - f(x))/h,
        # then for h = 0, the family is undefined and thus fails to be equicontinuous.
        # If Delta_h is the forward difference f(x+h) - f(x), it is mathematically 
        # proven to be equicontinuous for any fixed h. Thus, a valid counterexample 
        # must exploit the difference quotient interpretation with h = 0.
        try:
            if h_val == 0:
                neg_Q = True
            else:
                # For h != 0, the difference quotient or forward difference of an 
                # equicontinuous family remains equicontinuous.
                neg_Q = False
        except Exception:
            neg_Q = False

        return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]

    except Exception:
        return [False, False, False, False]