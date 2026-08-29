import math
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def minpoly_degree(M):
    k = M.shape[0]
    if k == 0:
        return 0
    I = eye(k)
    vecs = [I.reshape(k**2, 1)]
    for d in range(1, k+1):
        Md = M**d
        vecs.append(Md.reshape(k**2, 1))
        mat = Matrix.hstack(*vecs)
        if mat.rank() < d + 1:
            return d
    return k

def algebra_span(matrices):
    k = matrices[0].shape[0]
    basis = [eye(k).reshape(k**2, 1)]
    basis_mat = basis[0]
    rank = 1
    
    queue = [eye(k)]
    while queue:
        curr = queue.pop(0)
        for M in matrices:
            nxt = curr * M
            nxt_vec = nxt.reshape(k**2, 1)
            test_mat = Matrix.hstack(basis_mat, nxt_vec)
            new_rank = test_mat.rank()
            if new_rank > rank:
                basis.append(nxt_vec)
                basis_mat = test_mat
                rank = new_rank
                queue.append(nxt)
                if rank == k**2:
                    return basis_mat, rank
    return basis_mat, rank

def conditions(witness):
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha')
            beta = witness.get('beta')
            gamma = witness.get('gamma')
            m = witness.get('m')
            n = witness.get('n')
        else:
            alpha = getattr(witness, 'alpha', None)
            beta = getattr(witness, 'beta', None)
            gamma = getattr(witness, 'gamma', None)
            m = getattr(witness, 'm', None)
            n = getattr(witness, 'n', None)
            
        try:
            if not isinstance(alpha, Matrix):
                alpha = Matrix(alpha)
        except Exception:
            pass
        try:
            if not isinstance(beta, Matrix):
                beta = Matrix(beta)
        except Exception:
            pass
        try:
            if not isinstance(gamma, Matrix):
                gamma = Matrix(gamma)
        except Exception:
            pass

        # H_1
        h1 = False
        if isinstance(alpha, Matrix) and isinstance(beta, Matrix):
            if alpha.shape[0] == alpha.shape[1] and beta.shape[0] == beta.shape[1]:
                if alpha.shape == beta.shape:
                    h1 = True
                    
        if not h1:
            return [False] * 5 + [False]
            
        # H_2
        try:
            m_int = int(m)
            deg_alpha = minpoly_degree(alpha)
            h2 = (deg_alpha == m_int)
        except Exception:
            h2 = False
            
        # H_3
        try:
            n_int = int(n)
            deg_beta = minpoly_degree(beta)
            h3 = (deg_beta == n_int)
        except Exception:
            h3 = False
            
        # H_4
        try:
            h4 = (math.gcd(m_int, n_int) == 1)
        except Exception:
            h4 = False
            
        # H_5
        h5 = False
        try:
            if isinstance(gamma, Matrix) and gamma.shape == alpha.shape:
                span_AB, rank_AB = algebra_span([alpha, beta])
                span_G, rank_G = algebra_span([gamma])
                
                if rank_AB == rank_G:
                    k = alpha.shape[0]
                    mat_g = Matrix.hstack(span_AB, gamma.reshape(k**2, 1))
                    if mat_g.rank() == rank_AB:
                        mat_a = Matrix.hstack(span_G, alpha.reshape(k**2, 1))
                        mat_b = Matrix.hstack(span_G, beta.reshape(k**2, 1))
                        if mat_a.rank() == rank_G and mat_b.rank() == rank_G:
                            h5 = True
        except Exception:
            h5 = False
            
        # neg_Q
        neg_q = False
        try:
            deg_gamma = minpoly_degree(gamma)
            neg_q = (deg_gamma != m_int * n_int)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, h5, neg_q]
    except Exception:
        return [False] * 5 + [False]

CONDITION_LABELS = [
    "H_1: alpha and beta are elements of E that are algebraic over F",
    "H_2: The degree of the minimal polynomial of alpha over F is m",
    "H_3: The degree of the minimal polynomial of beta over F is n",
    "H_4: The integers m and n are coprime",
    "H_5: gamma is a primitive element such that F(alpha, beta) = F(gamma)",
    "¬Q: The degree of the minimal polynomial of gamma over F is not equal to mn"
]

N_HYP = 5
NEG_Q_INDEX = 5