import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    
    # H_1: A is positive definite
    # In the context of this false conjecture (where the "symmetric" hypothesis was dropped),
    # "positive definite" is evaluated using Sylvester's criterion (leading principal minors > 0),
    # which is a common misconception/flawed definition for non-symmetric matrices.
    def h1_ok(w):
        try:
            if not hasattr(w, "is_square") or not w.is_square:
                return False
            
            # 1. Try SymPy's built-in property/method (historical versions used Sylvester's criterion directly)
            try:
                res = w.is_positive_definite
                if callable(res):
                    res = res()
                if res is True:
                    return True
            except Exception:
                pass

            # 2. Fallback: explicitly check if all leading principal minors are strictly positive
            n = w.rows
            all_pos = True
            for i in range(1, n + 1):
                det_val = sympy.sympify(w[:i, :i].det())
                if det_val.is_positive is not True:
                    all_pos = False
                    break
            if all_pos:
                return True
                
        except Exception:
            pass
        return False

    # ¬Q: Every diagonal entry of A is strictly greater than zero (MUST FAIL)
    # Negation: At least one diagonal entry of A is NOT strictly greater than zero.
    def neg_q_ok(w):
        try:
            if not hasattr(w, "is_square") or not w.is_square:
                return False
            n = w.rows
            for i in range(n):
                val = sympy.sympify(w[i, i])
                # If the entry is not strictly positive (e.g., <= 0, complex, or symbolic), the conclusion fails.
                if val.is_positive is not True:
                    return True
            return False
        except Exception:
            return False

    return [h1_ok(witness), neg_q_ok(witness)]

CONDITION_LABELS = [
    "H_1: A is positive definite",
    "¬Q: At least one diagonal entry of A is not strictly greater than zero"
]

N_HYP = 1
NEG_Q_INDEX = 1