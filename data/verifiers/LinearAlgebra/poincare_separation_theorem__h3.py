import sympy as sp
from sympy import Matrix, re, im, eye
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is an n x n real symmetric matrix",
    "H_2: B is an n x k real matrix with B^T B = I_k",
    "¬Q: The inequalities lambda_i <= mu_i <= lambda_{n-k+i} fail for some i"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    res = [False, False, False]
    
    try:
        if len(witness) == 3:
            A, B, mu = witness
        else:
            return res
    except Exception:
        return res

    try:
        A_mat = Matrix(A)
        n = A_mat.rows
        h1 = (A_mat.cols == n) and A_mat.is_symmetric()
        if h1:
            for x in A_mat:
                if sp.simplify(im(x)) != 0:
                    h1 = False
                    break
        res[0] = bool(h1)
    except Exception:
        pass

    try:
        B_mat = Matrix(B)
        k = B_mat.cols
        h2 = False
        if B_mat.rows == n:
            BtB = B_mat.T * B_mat
            Ik = eye(k)
            diff = BtB - Ik
            h2_temp = True
            for x in diff:
                if sp.simplify(x) != 0:
                    h2_temp = False
                    break
            if h2_temp:
                for x in B_mat:
                    if sp.simplify(im(x)) != 0:
                        h2_temp = False
                        break
                h2 = h2_temp
        res[1] = bool(h2)
    except Exception:
        pass

    try:
        if res[0] and res[1]:
            evals_A = A_mat.eigenvals(multiple=True)
            evals_A = sorted([re(sp.simplify(e)) for e in evals_A])
            
            if hasattr(mu, '__len__') and len(mu) == k:
                holds_all = True
                for i in range(1, k+1):
                    lam_i = evals_A[i-1]
                    lam_n_k_i = evals_A[n-k+i-1]
                    m_i = re(sp.simplify(mu[i-1]))
                    
                    if not (bool(lam_i <= m_i) and bool(m_i <= lam_n_k_i)):
                        holds_all = False
                        break
                res[2] = not holds_all
    except Exception:
        pass

    return res