import sympy
from sympy import S, FiniteSet, ProductSet

# Top-level setup
# No specific named objects required for this real analysis domain,
# but standard symbols are available.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the dimension n and the subset A.
    """
    try:
        # Extract n and A from the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            n, A = witness
        else:
            n, A = None, witness
    except Exception:
        n, A = None, None

    # Check Hypothesis 1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    # Check Negated Conclusion: The complement R^n \ A is NOT path-connected
    try:
        neg_q = False
        if h1:
            # Hyperplanes represented as Cartesian products (e.g., R x {0} in R^2)
            if isinstance(A, ProductSet) and len(A.sets) == n:
                reals_count = 0
                finite_count = 0
                for s in A.sets:
                    if s == S.Reals:
                        reals_count += 1
                    elif isinstance(s, FiniteSet) and len(s) > 0:
                        finite_count += 1
                    elif hasattr(s, 'is_Interval') and s.is_Interval and s != S.Reals:
                        finite_count += 1
                
                # A hyperplane in R^n is homeomorphic to R^{n-1}, which separates R^n
                if reals_count == n - 1 and finite_count == 1:
                    neg_q = True
            
            # Standard geometry objects that separate space
            elif type(A).__name__ in ['Line', 'Line2D', 'Line3D', 'Plane', 'Circle', 'Sphere', 'Ellipse']:
                neg_q = True
                
            # Equations representing hypersurfaces (e.g., Eq(x, 0))
            elif isinstance(A, sympy.Eq):
                neg_q = True
                
            # String representations for simplicity
            elif isinstance(A, str):
                A_lower = A.lower()
                if any(word in A_lower for word in ['line', 'plane', 'sphere', 'circle', 'hyperplane', 'axis']):
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: The complement R^n \\ A is not path-connected"
]

N_HYP = 1
NEG_Q_INDEX = 1