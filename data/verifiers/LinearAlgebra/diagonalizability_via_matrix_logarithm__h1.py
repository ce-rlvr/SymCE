import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: A is non-singular
        h1 = bool(witness.det() != 0)
    except Exception:
        h1 = False

    try:
        # Check if the witness is a real matrix.
        # If it is complex, the conjecture (interpreted over C) is actually true,
        # so a valid counterexample must be a real matrix.
        is_real = True
        for e in witness:
            if getattr(e, "is_real", None) is not True:
                im_part = sp.im(e)
                if getattr(im_part, "is_zero", None) is not True:
                    is_real = False
                    break
        
        if not is_real:
            neg_q = False
        else:
            is_diag = True
            eigenvals_positive = True
            
            # Check diagonalizability over R and signs of eigenvalues
            for val, mult, vects in witness.eigenvects():
                # Eigenvalues must be real for diagonalizability over R
                if getattr(val, "is_real", None) is not True:
                    im_part = sp.im(val)
                    if getattr(im_part, "is_zero", None) is not True:
                        is_diag = False
                        break
                
                # Algebraic multiplicity must equal geometric multiplicity
                if len(vects) != mult:
                    is_diag = False
                    break
                
                # Check if the eigenvalue is strictly positive
                is_pos = getattr(val, "is_positive", None)
                if is_pos is False:
                    eigenvals_positive = False
                elif is_pos is None:
                    try:
                        if float(val) <= 0:
                            eigenvals_positive = False
                    except Exception:
                        eigenvals_positive = False
                        
            # P: A is diagonalizable (over R)
            p = is_diag
            
            # Q: There exists a diagonalizable matrix L (over R) such that e^L = A.
            # This is true over R iff A is diagonalizable over R AND all its eigenvalues are strictly positive.
            q = is_diag and eigenvals_positive
            
            # The conclusion is P <-> Q. The negated conclusion is P != Q.
            neg_q = bool(p != q)
            
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is non-singular",
    "¬Q: A is diagonalizable iff there exists a diagonalizable matrix L such that e^L = A is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1