import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is an n x n square matrix",
    "H_2: A is a normal matrix (A^* A = A A^*)",
    "¬Q: A is not unitarily diagonalizable over C"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conjugate_transpose(M):
    try:
        return M.H
    except Exception:
        pass
    
    try:
        M_T = M.T
        return M_T.applyfunc(lambda x: x.conjugate() if hasattr(x, 'conjugate') else x)
    except Exception:
        try:
            return M.T
        except Exception:
            return M

def is_zero_matrix(M):
    try:
        if hasattr(M, 'is_zero_matrix') and M.is_zero_matrix is True:
            return True
        
        for x in M:
            if x == 0:
                continue
            if hasattr(x, 'is_zero') and x.is_zero is True:
                continue
            if hasattr(x, 'expand') and x.expand() == 0:
                continue
            if sp.simplify(x) == 0:
                continue
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    # Pre-process witness to ensure it's a SymPy matrix
    try:
        if isinstance(witness, list):
            matrix_obj = sp.Matrix(witness)
        elif hasattr(witness, 'as_explicit'):
            matrix_obj = witness.as_explicit()
        elif hasattr(witness, 'to_Matrix'):
            matrix_obj = witness.to_Matrix()
        elif not isinstance(witness, sp.MatrixBase):
            matrix_obj = sp.Matrix(witness)
        else:
            matrix_obj = witness
    except Exception:
        matrix_obj = witness

    # H1: A is an n x n square matrix
    try:
        h1 = hasattr(matrix_obj, 'shape') and len(matrix_obj.shape) == 2 and matrix_obj.shape[0] == matrix_obj.shape[1]
    except Exception:
        h1 = False

    # H2: A is a normal matrix (A^* A = A A^*)
    try:
        if not h1:
            h2 = False
        else:
            A_star = conjugate_transpose(matrix_obj)
            diff = A_star * matrix_obj - matrix_obj * A_star
            h2 = is_zero_matrix(diff)
    except Exception:
        h2 = False

    # neg_Q: A is NOT unitarily diagonalizable over C
    try:
        if not h1:
            neg_q = False
        else:
            # A matrix is unitarily diagonalizable over C iff it is a complex normal matrix.
            # First, verify that all entries belong to the complex numbers.
            is_complex = True
            for x in matrix_obj:
                if isinstance(x, (int, float, complex)):
                    continue
                if hasattr(x, 'is_complex'):
                    if x.is_complex is False:
                        is_complex = False
                        break
                    continue
                # If it's a custom object without an is_complex attribute (e.g., finite field element)
                is_complex = False
                break
            
            if not is_complex:
                # If it's not a complex matrix, it cannot be factored into complex matrices U D U^*
                neg_q = True
            else:
                # For complex matrices, it is unitarily diagonalizable iff it is normal.
                A_star = conjugate_transpose(matrix_obj)
                diff = A_star * matrix_obj - matrix_obj * A_star
                is_normal = is_zero_matrix(diff)
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]