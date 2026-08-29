import sympy as sp
from sympy import eye, zeros, expand

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    try:
        if M == zeros(M.rows, M.cols): return True
        M = expand(M)
        if M == zeros(M.rows, M.cols): return True
        M = M.applyfunc(sp.cancel)
        if M == zeros(M.rows, M.cols): return True
        M = M.applyfunc(sp.simplify)
        return M == zeros(M.rows, M.cols)
    except Exception:
        return False

def conditions(witness):
    # H1: The entries of A are complex numbers
    try:
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        else:
            h1 = True
            for val in witness:
                if val.is_complex is False:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: A is a normal matrix
    try:
        if not witness.is_square:
            h2 = False
        else:
            diff = witness * witness.H - witness.H * witness
            h2 = is_zero_mat(diff)
    except Exception:
        h2 = False

    # Conclusion: A can be written as the sum over its distinct eigenvalues lambda_i of lambda_i * P_i, 
    # where each P_i is an orthogonal projection matrix, P_i P_j = 0 for i != j, 
    # and the sum of all P_i equals the identity matrix.
    try:
        if not witness.is_square:
            neg_q = True
        else:
            n = witness.rows
            I = eye(n)
            eigenvects = witness.eigenvects()
            
            P_list = []
            lambdas = []
            for val, mult, basis in eigenvects:
                from sympy.matrices import GramSchmidt
                ortho_basis = GramSchmidt(basis, orthonormal=False)
                
                P_i = zeros(n, n)
                for vec in ortho_basis:
                    norm_sq = (vec.H * vec)[0, 0]
                    P_i += (vec * vec.H) / norm_sq
                
                P_list.append(P_i)
                lambdas.append(val)
                
            conclusion_holds = True
            
            # 1. each P_i is an orthogonal projection matrix
            for P in P_list:
                if not is_zero_mat(P * P - P):
                    conclusion_holds = False
                if not is_zero_mat(P.H - P):
                    conclusion_holds = False
                    
            # 2. P_i P_j = 0 for i != j
            for i in range(len(P_list)):
                for j in range(len(P_list)):
                    if i != j:
                        if not is_zero_mat(P_list[i] * P_list[j]):
                            conclusion_holds = False
                            
            # 3. sum of all P_i equals the identity matrix
            sum_P = sum(P_list, zeros(n, n))
            if not is_zero_mat(sum_P - I):
                conclusion_holds = False
                
            # 4. A = sum lambda_i P_i
            sum_lP = zeros(n, n)
            for val, P in zip(lambdas, P_list):
                sum_lP += val * P
            if not is_zero_mat(sum_lP - witness):
                conclusion_holds = False
                
            neg_q = not conclusion_holds
    except Exception:
        # If spectral decomposition fails or cannot be verified, conclusion fails
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The entries of A are complex numbers",
    "H_2: A is a normal matrix",
    "¬Q: A cannot be written as the sum of lambda_i P_i with orthogonal projections P_i summing to I"
]

N_HYP = 2
NEG_Q_INDEX = 2