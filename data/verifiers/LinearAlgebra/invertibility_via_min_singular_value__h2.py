import sympy
from sympy.matrices import MatrixBase
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "Let A be an n x n complex matrix. A is invertible iff sigma_min(A) > 0."
    """
    # H_1: A is an n x n complex matrix
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        else:
            if witness.rows != witness.cols:
                h1 = False
            else:
                # Check if all entries are complex numbers (or symbols assumed complex)
                # For an empty matrix (0x0), all() vacuously returns True, which is correct.
                h1 = all(getattr(e, 'is_complex', False) for e in witness)
    except Exception:
        h1 = False

    # ¬Q: The conclusion FAILS at the witness
    # Conclusion: A is invertible iff sigma_min(A) > 0
    try:
        if not isinstance(witness, MatrixBase):
            neg_q = False
        else:
            # Check invertibility (det != 0)
            # For a 0x0 matrix, det is 1, so it is invertible.
            det_val = witness.det()
            is_inv = bool(det_val != 0)
            
            # Check minimum singular value
            sigmas = witness.singular_values()
            if not sigmas:
                # For a 0x0 matrix, there are no singular values.
                # The minimum is undefined, so the statement "sigma_min > 0" is False.
                sigma_min_gt_0 = False
            else:
                min_sigma = min(sigmas)
                try:
                    sigma_min_gt_0 = bool(min_sigma > 0)
                except TypeError:
                    # Fallback for symbolic expressions
                    sigma_min_gt_0 = min_sigma.is_positive
                    if sigma_min_gt_0 is None:
                        sigma_min_gt_0 = False
            
            # The conclusion is (is_inv == sigma_min_gt_0).
            # We want the negation of the conclusion.
            neg_q = bool(is_inv != sigma_min_gt_0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: A is invertible is not equivalent to sigma_min(A) > 0"
]

N_HYP = 1
NEG_Q_INDEX = 1