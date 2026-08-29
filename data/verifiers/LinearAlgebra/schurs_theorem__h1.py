import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Check if the matrix is real. If it has complex entries, it represents
            # an operator on a complex inner product space, where Schur's Theorem 
            # always holds (so it can be upper triangularized, meaning neg_q is False).
            is_real_matrix = True
            for elem in witness:
                if elem.is_real is False:
                    is_real_matrix = False
                    break
                elif elem.is_real is None:
                    try:
                        c = complex(elem)
                        if abs(c.imag) > 1e-9:
                            is_real_matrix = False
                            break
                    except Exception:
                        pass
            
            if not is_real_matrix:
                neg_q = False
            else:
                # For a real matrix (operator on a real inner product space), 
                # it can be upper triangularized via an orthonormal basis 
                # if and only if all its eigenvalues are real.
                evals = witness.eigenvals()
                all_real = True
                for val in evals:
                    if val.is_real is False:
                        all_real = False
                        break
                    elif val.is_real is None:
                        try:
                            c = complex(val)
                            if abs(c.imag) > 1e-9:
                                all_real = False
                                break
                        except Exception:
                            pass
                neg_q = not all_real
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V (represented as a square matrix)",
    "¬Q: There does not exist an orthonormal basis with respect to which the matrix of T is upper triangular"
]

N_HYP = 1
NEG_Q_INDEX = 1