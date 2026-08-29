import sympy
from sympy import eye, zeros
import z3

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_real_basis(basis):
    """
    Converts a basis of complex matrices to a basis of real block matrices
    using the standard embedding of M_n(C) into M_{2n}(R).
    """
    n = basis[0].shape[0]
    is_complex = False
    for B in basis:
        for i in range(n):
            for j in range(n):
                val = B[i, j]
                if hasattr(val, 'as_real_imag'):
                    _, im = val.as_real_imag()
                    if im != 0:
                        is_complex = True
                        break
            if is_complex: break
        if is_complex: break

    if not is_complex:
        return basis

    real_basis = []
    for B in basis:
        B_re = sympy.zeros(n, n)
        B_im = sympy.zeros(n, n)
        for i in range(n):
            for j in range(n):
                val = B[i, j]
                if hasattr(val, 'as_real_imag'):
                    re, im = val.as_real_imag()
                else:
                    re, im = val, 0
                B_re[i, j] = re
                B_im[i, j] = im
        top = sympy.Matrix.hstack(B_re, B_im)
        bottom = sympy.Matrix.hstack(-B_im, B_re)
        real_basis.append(sympy.Matrix.vstack(top, bottom))
    return real_basis

def is_reduced_algebra(basis):
    """
    Checks if the algebra spanned by the basis matrices is reduced
    (contains no non-zero nilpotent elements) using Z3.
    """
    real_basis = get_real_basis(basis)
    n = real_basis[0].shape[0]
    m = len(real_basis)
    
    solver = z3.Solver()
    c = [z3.Real(f'c_{i}') for i in range(m)]
    
    M = [[0 for _ in range(n)] for _ in range(n)]
    for k, B in enumerate(real_basis):
        for i in range(n):
            for j in range(n):
                val = B[i, j]
                if val == 0:
                    continue
                if val.is_Integer:
                    M[i][j] += int(val) * c[k]
                elif val.is_Rational:
                    M[i][j] += (int(val.p) / int(val.q)) * c[k]
                else:
                    M[i][j] += float(val) * c[k]
                    
    def mat_mul(A, B_mat):
        res = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                res[i][j] = sum(A[i][k] * B_mat[k][j] for k in range(n))
        return res

    M_pow = M
    for _ in range(n - 1):
        M_pow = mat_mul(M_pow, M)
        
    for i in range(n):
        for j in range(n):
            solver.add(M_pow[i][j] == 0)
            
    m_not_zero = []
    for i in range(n):
        for j in range(n):
            m_not_zero.append(M[i][j] != 0)
    solver.add(z3.Or(m_not_zero))
    
    solver.set("timeout", 2000)
    
    res = solver.check()
    if res == z3.unknown:
        return False
    return res == z3.unsat

def in_span(A, basis):
    """
    Checks if matrix A is in the linear span of the basis matrices.
    """
    vecs = [B.vec() for B in basis]
    A_vec = A.vec()
    M = sympy.Matrix.hstack(*vecs)
    M_aug = sympy.Matrix.hstack(M, A_vec)
    return M.rank() == M_aug.rank()

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            basis = witness.get('basis')
            e = witness.get('e')
            x = witness.get('x')
        else:
            basis = getattr(witness, 'basis', None)
            e = getattr(witness, 'e', None)
            x = getattr(witness, 'x', None)
            
        if basis is None or e is None or x is None:
            return [False, False, False, False]
            
        if not isinstance(basis, list) or len(basis) == 0:
            return [False, False, False, False]
            
        n = basis[0].shape[0]
        if any(not hasattr(B, 'shape') or B.shape != (n, n) for B in basis):
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring
    try:
        I = sympy.eye(n)
        if not in_span(I, basis):
            h1 = False
        else:
            closed = True
            for B1 in basis:
                for B2 in basis:
                    if not in_span(B1 * B2, basis):
                        closed = False
                        break
                if not closed:
                    break
            h1 = closed
    except Exception:
        h1 = False

    # H2: R is a reduced ring
    try:
        h2 = is_reduced_algebra(basis)
    except Exception:
        h2 = False

    # H3: x is an element of R
    try:
        h3 = in_span(x, basis)
    except Exception:
        h3 = False

    # neg_Q: ex != xe
    try:
        neg_q = bool(e * x != x * e)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a reduced ring",
    "H_3: x is an element of R",
    "¬Q: ex != xe"
]

N_HYP = 3
NEG_Q_INDEX = 3