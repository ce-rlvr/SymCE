import sympy
from sympy import eye, zeros, Matrix
from sympy.abc import x

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: W is a T-invariant subspace of V",
    "H_3: lambda is a complex number that is not an eigenvalue of T",
    "¬Q: W is not invariant under the resolvent operator (T - lambda I)^-1"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the Resolvent Operator Invariance Theorem.
    The witness is expected to be a tuple (T, W, lam) where T and W are SymPy matrices and lam is a scalar.
    To represent an infinite-dimensional space, T and W can have polynomial entries (e.g., using symbol 'x'),
    effectively treating V as a free module over C[x].
    """
    try:
        T, W, lam = witness
    except Exception:
        # Fallback for custom witness objects
        try:
            h1 = witness.is_linear_operator()
            h2 = witness.is_T_invariant()
            h3 = not witness.is_eigenvalue()
            neg_q = not witness.is_resolvent_invariant()
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
        except Exception:
            return [False, False, False, False]

    def is_in_span(W_mat, V_target):
        """
        Checks if V_target is in the column span of W_mat over the polynomial ring.
        This allows finite matrices to simulate infinite-dimensional spaces over C.
        """
        try:
            # Check if it's in the span over the field of fractions
            if W_mat.rank() != W_mat.row_join(V_target).rank():
                return False
            
            # Solve for the coefficients
            try:
                X = W_mat.solve(V_target)
            except Exception:
                # If solve fails (e.g., not full column rank), use a basis
                W_basis = Matrix.hstack(*W_mat.columnspace())
                X = W_basis.solve(V_target)
                
            # Check if all coefficients are polynomials (denominators must be constant)
            for element in X:
                num, den = element.cancel().as_numer_denom()
                if not den.is_constant():
                    return False
            return True
        except Exception:
            return False

    # H_1: T is a linear operator on V
    try:
        h1 = hasattr(T, 'is_square') and T.is_square
    except Exception:
        h1 = False

    # H_2: W is a T-invariant subspace of V
    try:
        h2 = is_in_span(W, T * W)
    except Exception:
        h2 = False

    # H_3: lambda is a complex number that is not an eigenvalue of T
    try:
        # Check if lam is a scalar (should not contain symbolic variables like x)
        if hasattr(lam, 'free_symbols') and len(lam.free_symbols) > 0:
            h3 = False
        else:
            I = eye(T.rows)
            # Not an eigenvalue means det(T - lam * I) != 0
            h3 = (T - lam * I).det() != 0
    except Exception:
        h3 = False

    # ¬Q: W is not invariant under the resolvent operator (T - lambda I)^-1
    try:
        I = eye(T.rows)
        resolvent = (T - lam * I).inv()
        neg_q = not is_in_span(W, resolvent * W)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]