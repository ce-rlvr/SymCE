import sympy
from sympy import Symbol, simplify, expand, BlockMatrix, Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M is a block upper triangular matrix with square diagonal blocks A and B",
    "H_2: p_A(x) and p_B(x) are the characteristic polynomials of A and B respectively",
    "¬Q: p_M(x) != p_A(x) p_B(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(witness):
    if isinstance(witness, dict):
        if 'pA' in witness:
            return witness['M'], witness['A'], witness['B'], witness['pA'], witness['pB'], witness.get('x', Symbol('x'))
        else:
            return witness['M'], witness['A'], witness['B']
    return witness

def is_zero_mat(mat):
    if hasattr(mat, 'is_zero_matrix') and mat.is_zero_matrix:
        return True
    try:
        for i in range(mat.rows):
            for j in range(mat.cols):
                if expand(mat[i, j]) != 0:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        elements = get_elements(witness)
        if len(elements) == 3:
            M, A, B = elements
            x = Symbol('x')
            pA = A.charpoly(x).as_expr()
            pB = B.charpoly(x).as_expr()
        elif len(elements) == 6:
            M, A, B, pA, pB, x = elements
            pA = pA.as_expr() if hasattr(pA, 'as_expr') else pA
            pB = pB.as_expr() if hasattr(pB, 'as_expr') else pB
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: M is a block upper triangular matrix with square diagonal blocks A and B
    h1_ok = False
    try:
        if isinstance(M, BlockMatrix):
            is_upper_tri = (M.blockshape[0] == M.blockshape[1])
            if is_upper_tri:
                for i in range(M.blockshape[0]):
                    for j in range(i):
                        if not is_zero_mat(M.blocks[i, j]):
                            is_upper_tri = False
                            break
            
            if is_upper_tri and A.rows == A.cols and B.rows == B.cols:
                diag_blocks = [M.blocks[i, i] for i in range(M.blockshape[0])]
                found = False
                for i in range(len(diag_blocks)):
                    for j in range(len(diag_blocks)):
                        if i != j and diag_blocks[i] == A and diag_blocks[j] == B:
                            found = True
                h1_ok = found
        else:
            n = M.rows
            if M.cols == n and A.rows == A.cols and B.rows == B.cols:
                # Check k=2 partition
                found = False
                for s1 in range(1, n):
                    if is_zero_mat(M[s1:, :s1]):
                        d1 = M[:s1, :s1]
                        d2 = M[s1:, s1:]
                        if (d1 == A and d2 == B) or (d1 == B and d2 == A):
                            found = True
                            break
                if not found:
                    # Check k=3 partition
                    for s1 in range(1, n):
                        for s2 in range(1, n - s1):
                            if is_zero_mat(M[s1:, :s1]) and is_zero_mat(M[s1+s2:, :s1+s2]):
                                d1 = M[:s1, :s1]
                                d2 = M[s1:s1+s2, s1:s1+s2]
                                d3 = M[s1+s2:, s1+s2:]
                                diags = [d1, d2, d3]
                                for i in range(3):
                                    for j in range(3):
                                        if i != j and diags[i] == A and diags[j] == B:
                                            found = True
                h1_ok = found
    except Exception:
        h1_ok = False

    # H2: p_A(x) and p_B(x) are the characteristic polynomials of A and B respectively
    h2_ok = False
    try:
        expr_A = A.charpoly(x).as_expr()
        expr_B = B.charpoly(x).as_expr()
        h2_ok = (expand(expr_A - pA) == 0) and (expand(expr_B - pB) == 0)
    except Exception:
        h2_ok = False

    # neg_Q: p_M(x) != p_A(x) p_B(x)
    neg_q_ok = False
    try:
        if isinstance(M, BlockMatrix):
            M_explicit = M.as_explicit()
        else:
            M_explicit = M
        pM = M_explicit.charpoly(x).as_expr()
        diff = expand(pM - pA * pB)
        neg_q_ok = (diff != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]