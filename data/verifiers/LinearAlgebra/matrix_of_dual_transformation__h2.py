import sympy
from sympy import Matrix, S

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_permutation_matrix(M):
    if M.shape[0] != M.shape[1]: 
        return False
    n = M.shape[0]
    for i in range(n):
        row_sum = 0
        for j in range(n):
            val = M[i, j]
            if val == 1 or val == S.One:
                row_sum += 1
            elif val == 0 or val == S.Zero:
                pass
            else:
                val = sympy.simplify(val)
                if val == 1:
                    row_sum += 1
                elif val != 0:
                    return False
        if row_sum != 1:
            return False
    for j in range(n):
        col_sum = 0
        for i in range(n):
            val = M[i, j]
            if val == 1 or val == S.One:
                col_sum += 1
            elif val == 0 or val == S.Zero:
                pass
            else:
                val = sympy.simplify(val)
                if val == 1:
                    col_sum += 1
                elif val != 0:
                    return False
        if col_sum != 1:
            return False
    return True

def conditions(witness):
    try:
        T = Matrix(witness['T'])
        beta = [Matrix(b) for b in witness['beta']]
        gamma = [Matrix(g) for g in witness['gamma']]
        n = len(beta)
        m = len(gamma)
        
        beta = [b.reshape(n, 1) for b in beta]
        gamma = [g.reshape(m, 1) for g in gamma]
        
        beta_star = [Matrix(b).reshape(1, n) for b in witness['beta_star']]
        gamma_star = [Matrix(g).reshape(1, m) for g in witness['gamma_star']]
        
        h1 = False
        if n > 0 and m > 0:
            B = Matrix.hstack(*beta)
            G = Matrix.hstack(*gamma)
            
            if B.shape == (n, n) and G.shape == (m, m):
                if B.det() != 0 and G.det() != 0:
                    B_star = Matrix.vstack(*beta_star)
                    G_star = Matrix.vstack(*gamma_star)
                    
                    if B_star.shape == (n, n) and G_star.shape == (m, m):
                        P_B = B_star * B
                        P_G = G_star * G
                        if is_permutation_matrix(P_B) and is_permutation_matrix(P_G):
                            h1 = True
    except Exception:
        h1 = False

    try:
        T = Matrix(witness['T'])
        n = len(witness['beta'])
        m = len(witness['gamma'])
        
        h2 = False
        if T.shape == (m, n):
            h2 = True
    except Exception:
        h2 = False

    try:
        T = Matrix(witness['T'])
        beta = [Matrix(b) for b in witness['beta']]
        gamma = [Matrix(g) for g in witness['gamma']]
        n = len(beta)
        m = len(gamma)
        
        beta = [b.reshape(n, 1) for b in beta]
        gamma = [g.reshape(m, 1) for g in gamma]
        beta_star = [Matrix(b).reshape(1, n) for b in witness['beta_star']]
        gamma_star = [Matrix(g).reshape(1, m) for g in witness['gamma_star']]
        
        B = Matrix.hstack(*beta)
        G = Matrix.hstack(*gamma)
        B_star = Matrix.vstack(*beta_star)
        G_star = Matrix.vstack(*gamma_star)
        
        M_T = G.inv() * T * B
        
        B_star_T = B_star.transpose()
        G_star_T = G_star.transpose()
        
        M_T_star = B_star_T.inv() * T.transpose() * G_star_T
        
        eq = M_T_star.equals(M_T.transpose())
        if eq is None:
            neg_q = (M_T_star != M_T.transpose())
        else:
            neg_q = not eq
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are finite-dimensional vector spaces over a field F",
    "H_2: T: V \\to W is a linear transformation",
    "¬Q: The matrix representation of T^* relative to gamma^* and beta^* is not the transpose of the matrix representation of T relative to beta and gamma"
]

N_HYP = 2
NEG_Q_INDEX = 2