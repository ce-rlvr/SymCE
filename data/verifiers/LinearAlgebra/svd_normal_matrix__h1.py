import sympy
from sympy import Matrix, eye, zeros
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is a square matrix
    try:
        A = Matrix(witness)
        h1 = A.is_square
    except Exception:
        h1 = False

    # neg_Q: The singular values of A are NOT exactly the absolute values of its eigenvalues
    try:
        if not h1:
            neg_q = False
        else:
            # The singular values of A are the square roots of the eigenvalues of A.H * A.
            # We compare the multisets of the squares of the absolute values of the eigenvalues
            # with the multisets of the squares of the singular values.
            evs = A.eigenvals(multiple=True)
            abs_evs_sq = [(abs(ev)**2).evalf(50) for ev in evs]
            
            svs_sq = (A.H * A).eigenvals(multiple=True)
            svs_sq_eval = [sv.evalf(50) for sv in svs_sq]
            
            try:
                # Sort by real part (imaginary part should be 0 or negligible)
                abs_evs_sq.sort(key=lambda x: complex(x).real)
                svs_sq_eval.sort(key=lambda x: complex(x).real)
            except TypeError:
                # If conversion to complex fails (e.g., symbolic entries), we cannot verify
                neg_q = False
            else:
                if len(abs_evs_sq) != A.rows or len(svs_sq_eval) != A.rows:
                    neg_q = False
                else:
                    eval_success = True
                    match = True
                    for a, b in zip(abs_evs_sq, svs_sq_eval):
                        try:
                            ca = complex(a)
                            cb = complex(b)
                        except TypeError:
                            eval_success = False
                            break
                        
                        # Compare with a tolerance suitable for 50 decimal places of precision
                        if abs(ca - cb) > 1e-30:
                            match = False
                            break
                    
                    if not eval_success:
                        neg_q = False
                    else:
                        neg_q = not match
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The singular values of A are not exactly the absolute values of its eigenvalues"
]

N_HYP = 1
NEG_Q_INDEX = 1