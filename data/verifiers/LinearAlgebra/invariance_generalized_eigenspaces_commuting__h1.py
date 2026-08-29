import sympy
from sympy import eye, simplify, zeros
from sympy.matrices import Matrix

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      1. A and B commute
      2. \lambda is an eigenvalue of A
      3. V_\lambda is the generalized eigenspace of A corresponding to \lambda
    Conclusion:
      V_\lambda is an invariant subspace under B
    """
    try:
        # Witness can be (A, B, lambda_val) or (A, B, lambda_val, V_lambda)
        if len(witness) == 3:
            A, B, lambda_val = witness
            V_lambda_provided = None
        elif len(witness) == 4:
            A, B, lambda_val, V_lambda_provided = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: A and B commute
    try:
        diff = A * B - B * A
        h1 = False
        if diff.is_zero_matrix:
            h1 = True
        elif diff.expand().is_zero_matrix:
            h1 = True
        elif diff.simplify().is_zero_matrix:
            h1 = True
    except Exception:
        h1 = False

    # H_2: lambda is an eigenvalue of A
    try:
        if hasattr(lambda_val, 'is_Matrix') and lambda_val.is_Matrix:
            h2 = False
        else:
            n = A.shape[0]
            I = eye(n)
            M_base = A - lambda_val * I
            det_val = M_base.det()
            if det_val == 0 or det_val.expand() == 0 or det_val.simplify() == 0:
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: V_lambda is the generalized eigenspace of A corresponding to lambda
    try:
        if h2:
            # The generalized eigenspace is the nullspace of (A - \lambda I)^n
            M = M_base**n
            V_lambda = M.nullspace()
            h3 = True
            
            # If the witness explicitly provided a basis for V_lambda, verify it spans the same space
            if V_lambda_provided is not None:
                if len(V_lambda_provided) != len(V_lambda):
                    h3 = False
                else:
                    for v in V_lambda_provided:
                        res = M * v
                        if not (res.is_zero_matrix or res.expand().is_zero_matrix or res.simplify().is_zero_matrix):
                            h3 = False
                            break
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: V_lambda is NOT invariant under B
    try:
        if h3:
            invariant = True
            for v in V_lambda:
                Bv = B * v
                # Check if Bv is in V_lambda (i.e., annihilated by M)
                res = M * Bv
                if not (res.is_zero_matrix or res.expand().is_zero_matrix or res.simplify().is_zero_matrix):
                    invariant = False
                    break
            neg_q = not invariant
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and B commute",
    "H_2: lambda is an eigenvalue of A",
    "H_3: V_lambda is the generalized eigenspace of A corresponding to lambda",
    "¬Q: V_lambda is not invariant under B"
]

N_HYP = 3
NEG_Q_INDEX = 3