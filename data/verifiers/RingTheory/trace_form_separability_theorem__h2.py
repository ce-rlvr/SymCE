import sympy
from sympy import Poly, Matrix, QQ, ZZ, GF
from sympy.abc import x

# Top-level setup
# x is imported from sympy.abc to be used in witness expressions
# QQ, ZZ, GF are imported for domain specifications

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The witness is expected to be a sympy.Poly object representing f(x).
    """
    try:
        if not isinstance(witness, Poly):
            witness = Poly(witness)
    except Exception:
        pass

    # H_1: F is a field
    try:
        h1 = bool(witness.domain.is_Field)
    except Exception:
        h1 = False

    # H_2: A is a finite-dimensional F-algebra
    try:
        h2 = bool(witness.degree() >= 1)
    except Exception:
        h2 = False

    # neg_Q: The trace form is non-degenerate iff f(x) is a separable polynomial over F (fails)
    try:
        # 1. Compute the determinant of the trace form
        f = witness.monic()
        n = f.degree()
        coeffs = f.all_coeffs()
        a = coeffs[::-1] # a[0] is constant term, a[n] is 1
        
        domain = f.domain
        p = [domain.zero] * (2*n - 1)
        p[0] = domain.convert(n)
        
        # Newton's sums to find traces of powers of x
        for k in range(1, 2*n - 1):
            s = domain.zero
            if k <= n:
                for i in range(1, k):
                    s += a[n-i] * p[k-i]
                s += domain.convert(k) * a[n-k]
            else:
                for i in range(1, n + 1):
                    s += a[n-i] * p[k-i]
            p[k] = -s
            
        # Build the trace matrix [Tr(x^{i+j})]
        matrix = Matrix(n, n, lambda i, j: p[i+j])
        det = matrix.det()
        is_non_degenerate = bool(det)
        
        # 2. Check if f(x) is a separable polynomial
        # A polynomial is separable if all its irreducible factors are separable
        _, factors = witness.factor_list()
        is_separable_poly = True
        for factor_poly, mult in factors:
            deriv = factor_poly.diff()
            if deriv.is_zero:
                is_separable_poly = False
                break
                
        # The conclusion states they are equivalent
        conclusion = (is_non_degenerate == is_separable_poly)
        
        # We want the conclusion to FAIL
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is a finite-dimensional F-algebra",
    "¬Q: Trace form is non-degenerate iff f is separable"
]

N_HYP = 2
NEG_Q_INDEX = 2