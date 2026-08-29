import sympy
from sympy import Matrix, eye, zeros, diag, BlockDiagMatrix, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M is a block diagonal matrix over an algebraically closed field F",
    "¬Q: The Jordan canonical form of M is not similar to the direct sum of the Jordan canonical forms of A and B"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            M, A, B = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: M is a block diagonal matrix
    h1_ok = False
    try:
        if isinstance(M, BlockDiagMatrix):
            h1_ok = True
        else:
            M_mat = M.as_explicit() if hasattr(M, 'as_explicit') else M
            if hasattr(M_mat, 'rows') and hasattr(M_mat, 'cols') and M_mat.rows == M_mat.cols:
                n = M_mat.rows
                if n < 2:
                    h1_ok = True
                else:
                    def is_zero(val):
                        try:
                            if hasattr(val, 'is_zero') and val.is_zero is not None:
                                return val.is_zero
                            return bool(val == 0)
                        except Exception:
                            return False

                    for k in range(1, n):
                        upper_zero = all(is_zero(M_mat[i, j]) for i in range(k) for j in range(k, n))
                        lower_zero = all(is_zero(M_mat[i, j]) for i in range(k, n) for j in range(k))
                        if upper_zero and lower_zero:
                            h1_ok = True
                            break
    except Exception:
        h1_ok = False

    # neg_Q: JCF(M) is not similar to JCF(A) \oplus JCF(B)
    neg_q_ok = False
    try:
        A_mat = A.as_explicit() if hasattr(A, 'as_explicit') else A
        B_mat = B.as_explicit() if hasattr(B, 'as_explicit') else B
        M_mat = M.as_explicit() if hasattr(M, 'as_explicit') else M
        
        if A_mat.is_square and B_mat.is_square and M_mat.is_square:
            if M_mat.rows != A_mat.rows + B_mat.rows:
                neg_q_ok = True
            else:
                from sympy import default_sort_key
                N = diag(A_mat, B_mat)
                
                def get_jordan_blocks(mat):
                    P, J = mat.jordan_form()
                    blocks = []
                    n = J.rows
                    i = 0
                    while i < n:
                        val = J[i, i]
                        size = 1
                        while i + size < n and J[i + size, i + size] == val and J[i + size - 1, i + size] == 1:
                            size += 1
                        blocks.append((val, size))
                        i += size
                    return sorted(blocks, key=lambda x: (default_sort_key(x[0]), x[1]))
                    
                if get_jordan_blocks(M_mat) != get_jordan_blocks(N):
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]