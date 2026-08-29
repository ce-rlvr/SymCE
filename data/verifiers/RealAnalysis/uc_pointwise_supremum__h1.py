import sympy as sp

# Top-level setup for potential witness expressions
x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The conjecture is false because it omits the hypothesis that the family F is non-empty.
    If F is empty, the pointwise supremum is -infinity, which is not a real-valued function.
    """
    try:
        # Extract the family of functions from the witness
        if isinstance(witness, dict):
            family = witness.get('family', witness.get('F', witness))
        else:
            family = witness
            
        # We expect the family to be represented as a list, set, or tuple
        if not isinstance(family, (list, set, tuple)):
            return [False, False, False]
            
        # H_1: F is a uniformly equicontinuous family of real-valued functions on X.
        # An empty family is vacuously uniformly equicontinuous.
        h1 = True
        for f in family:
            try:
                expr = sp.sympify(f)
                # Basic heuristic check: polynomials of degree > 1 are not uniformly continuous on R
                if expr.is_polynomial(x) and sp.degree(expr, x) > 1:
                    h1 = False
                    break
            except Exception:
                h1 = False
                break
                
        # H_2: For every x in X, the set {f(x) : f in F} is bounded above.
        # An empty set is bounded above by any real number.
        # Any finite set of real-valued functions evaluated at x is bounded above.
        h2 = True
        
        # ¬Q: The pointwise supremum function g is not a uniformly continuous real-valued function on X.
        # If F is empty, g(x) = sup(empty) = -oo, which is not in R, so the conclusion fails (¬Q is True).
        # If F is non-empty, the conclusion mathematically holds (g is uniformly continuous), so ¬Q is False.
        neg_q = (len(family) == 0)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a uniformly equicontinuous family of real-valued functions on X",
    "H_2: For every x in X, the set {f(x) : f in F} is bounded above",
    "¬Q: The pointwise supremum function g is not a uniformly continuous real-valued function on X"
]

N_HYP = 2
NEG_Q_INDEX = 2