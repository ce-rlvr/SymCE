import sympy
from sympy import MatrixBase, Integer, Rational, sqrt, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_exact_rat(val):
    """Check if a value is an exact rational number (int, sympy.Integer, or sympy.Rational)."""
    return isinstance(val, (int, Integer, Rational))

def conditions(witness) -> list[bool]:
    try:
        # Witness can be a dictionary or a tuple
        if isinstance(witness, dict):
            A = witness.get('A')
            A_prime = witness.get("A'") if "A'" in witness else witness.get('A_prime')
        else:
            A, A_prime = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        # H1: V is a finite-dimensional vector space over a field F
        # We enforce F = Q by checking that all matrix entries are exact rationals.
        h1 = (isinstance(A, MatrixBase) and isinstance(A_prime, MatrixBase) and 
              A.is_square and A_prime.is_square and 
              A.shape == A_prime.shape and 
              0 < A.shape[0] <= 10)
        if h1:
            h1 = all(is_exact_rat(x) for x in A) and all(is_exact_rat(x) for x in A_prime)
    except Exception:
        h1 = False

    # H2: B is a bilinear form on V
    # Any square matrix over F defines a valid bilinear form on V.
    h2 = h1

    # H3: A' is the matrix representation of B with respect to a second basis of V
    # Since A' is a square matrix over F, it is a valid matrix representation of some bilinear form.
    h3 = h1

    try:
        if not h1:
            neg_q = False
        else:
            det_A = A.det()
            det_A_prime = A_prime.det()
            
            if det_A == 0:
                if det_A_prime == 0:
                    # 0 = c^2 * 0 holds for any non-zero c (e.g., c=1). Conclusion is TRUE.
                    neg_q = False
                else:
                    # det_A_prime = c^2 * 0 = 0, but det_A_prime != 0. Impossible. Conclusion FAILS.
                    neg_q = True
            else:
                ratio = det_A_prime / det_A
                if ratio < 0:
                    # No real (and thus no rational) square root exists. Conclusion FAILS.
                    neg_q = True
                elif ratio == 0:
                    # 0 = c^2 * det_A => c = 0, but we need a NON-ZERO c. Conclusion FAILS.
                    neg_q = True
                else:
                    # Check if there is a rational c such that c^2 = ratio
                    r = sqrt(ratio)
                    # If r is not an exact rational, then no such c exists in Q. Conclusion FAILS.
                    neg_q = not is_exact_rat(r)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a bilinear form on V",
    "H_3: A' is the matrix representation of B with respect to a second basis of V",
    "¬Q: There does not exist a non-zero element c in F such that det(A') = c^2 det(A)"
]

N_HYP = 3
NEG_Q_INDEX = 3