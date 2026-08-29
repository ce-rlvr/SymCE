import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an m x n complex matrix
    try:
        if not isinstance(witness, sp.MatrixBase):
            matrix_A = sp.Matrix(witness)
        else:
            matrix_A = witness
            
        h1 = True
        for val in matrix_A:
            # Check if the element is explicitly not complex (e.g., infinity)
            if val.is_complex is False:
                h1 = False
                break
    except Exception:
        h1 = False

    # neg_Q: The singular values of A^T are NOT identical to the singular values of A
    try:
        if not isinstance(witness, sp.MatrixBase):
            matrix_A = sp.Matrix(witness)
        else:
            matrix_A = witness
            
        # The singular values of an m x n matrix A are the square roots of the 
        # eigenvalues of the n x n matrix A^* A.
        mat_A = matrix_A.H * matrix_A
        evs_A = mat_A.eigenvals(multiple=True)
        
        # The singular values of A^T (which is n x m) are the square roots of the 
        # eigenvalues of the m x m matrix (A^T)^* A^T.
        mat_AT = matrix_A.T.H * matrix_A.T
        evs_AT = mat_AT.eigenvals(multiple=True)
        
        # If the lists of singular values have different lengths (i.e., m != n),
        # they cannot be identical.
        if len(evs_A) != len(evs_AT):
            neg_q = True
        else:
            # If they have the same length, we sort and compare them.
            def sort_key(x):
                try:
                    return float(sp.re(sp.N(x)))
                except Exception:
                    return 0.0
            
            evs_A_sorted = sorted(evs_A, key=sort_key, reverse=True)
            evs_AT_sorted = sorted(evs_AT, key=sort_key, reverse=True)
            
            identical = True
            for a, b in zip(evs_A_sorted, evs_AT_sorted):
                diff = sp.simplify(a - b)
                if diff != 0:
                    try:
                        # Allow for minor floating point inaccuracies
                        if abs(complex(diff)) > 1e-9:
                            identical = False
                            break
                    except Exception:
                        # If it cannot be cast to complex (e.g., symbolic difference), assume not identical
                        identical = False
                        break
            neg_q = not identical
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: The singular values of A^T are not identical to the singular values of A"
]

N_HYP = 1
NEG_Q_INDEX = 1