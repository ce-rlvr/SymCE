import sympy as sp
from sympy import eye, zeros

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: V is a finite-dimensional vector space over the complex numbers
    # In the context of matrix representations, any SymPy matrix represents a linear map 
    # between finite-dimensional vector spaces over the complex numbers (or a subfield).
    try:
        h1 = isinstance(witness, sp.MatrixBase)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails.
    # Conclusion: T is diagonalizable if and only if for every eigenvalue \lambda of T, 
    # the generalized eigenspace corresponding to \lambda is equal to the eigenspace corresponding to \lambda.
    try:
        if not isinstance(witness, sp.MatrixBase):
            neg_q = False
        else:
            if not witness.is_square:
                # A non-square matrix is not an endomorphism, so it is not diagonalizable.
                lhs = False
                # A non-square matrix has no eigenvalues, so the universal quantification 
                # "for every eigenvalue..." is vacuously true.
                rhs = True
            else:
                lhs = witness.is_diagonalizable()
                evs = witness.eigenvects()
                rhs = True
                for ev, alg_mult, evecs in evs:
                    # The generalized eigenspace dimension is the algebraic multiplicity.
                    # The eigenspace dimension is the geometric multiplicity (number of eigenvectors).
                    # Since the eigenspace is a subspace of the generalized eigenspace, 
                    # they are equal if and only if their dimensions are equal.
                    if alg_mult != len(evecs):
                        rhs = False
                        break
            
            # The conclusion is the biconditional (lhs <-> rhs)
            q = (lhs == rhs)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over the complex numbers",
    "¬Q: T is not diagonalizable, but vacuously satisfies the eigenspace condition (or vice versa)"
]

N_HYP = 1
NEG_Q_INDEX = 1