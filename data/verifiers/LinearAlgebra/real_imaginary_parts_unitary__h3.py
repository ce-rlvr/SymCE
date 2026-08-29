import sympy as sp

# Top-level setup for standard objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        # The dropped hypothesis is that A and B are real matrices.
        # A witness can be provided as (A, B), (U, A, B), or just U.
        if isinstance(witness, tuple):
            if len(witness) == 3:
                U, A, B = witness
                U = sp.Matrix(U)
                A = sp.Matrix(A)
                B = sp.Matrix(B)
            elif len(witness) == 2:
                A, B = witness
                A = sp.Matrix(A)
                B = sp.Matrix(B)
                U = A + sp.I * B
            else:
                return [False, False, False]
        else:
            # Fallback if only U is provided: we set A = U and B = 0.
            # If U is unitary but not orthogonal, A^T A + B^T B = U^T U != I,
            # which correctly violates the conclusion.
            U = sp.Matrix(witness)
            A = U
            B = sp.zeros(U.shape[0], U.shape[1])
            
        # H1: U is an n x n complex matrix
        if not hasattr(U, 'is_square') or not U.is_square or U.shape[0] == 0:
            h1 = False
        else:
            h1 = True
            
        # H2: U is a unitary matrix
        if h1:
            I_mat = sp.eye(U.shape[0])
            diff = sp.expand(U.H * U - I_mat)
            if diff.is_zero_matrix:
                h2 = True
            else:
                diff = sp.simplify(diff)
                h2 = (diff.is_zero_matrix == True)
        else:
            h2 = False
            
        # neg_Q: A^T A + B^T B != I or A^T B != B^T A
        if h1:
            I_mat_A = sp.eye(A.shape[0])
            
            eq1_diff = sp.expand(A.T * A + B.T * B - I_mat_A)
            if eq1_diff.is_zero_matrix:
                eq1 = True
            else:
                eq1_diff = sp.simplify(eq1_diff)
                eq1 = (eq1_diff.is_zero_matrix == True)
                
            eq2_diff = sp.expand(A.T * B - B.T * A)
            if eq2_diff.is_zero_matrix:
                eq2 = True
            else:
                eq2_diff = sp.simplify(eq2_diff)
                eq2 = (eq2_diff.is_zero_matrix == True)
                
            neg_q = not (eq1 and eq2)
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "H_2: U is a unitary matrix",
    "not Q: A^T A + B^T B != I or A^T B != B^T A"
]

N_HYP = 2
NEG_Q_INDEX = 2