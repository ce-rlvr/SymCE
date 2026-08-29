import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a vector space and B is a symmetric bilinear form on V",
    "H_2: T is a linear operator on V, self-adjoint with respect to B",
    "H_3: \\lambda and \\mu are distinct eigenvalues of T",
    "H_4: v and w are eigenvectors of T",
    "¬Q: The eigenvectors v and w are not orthogonal with respect to B (B(v, w) != 0)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            B = Matrix(witness['B'])
            T = Matrix(witness['T'])
            lam = witness['lam']
            mu = witness['mu']
            v = Matrix(witness['v'])
            w = Matrix(witness['w'])
        else:
            B, T, lam, mu, v, w = witness
            B = Matrix(B)
            T = Matrix(T)
            v = Matrix(v)
            w = Matrix(w)
            
        # Ensure v and w are column vectors
        if v.shape[0] == 1 and v.shape[1] > 1:
            v = v.T
        if w.shape[0] == 1 and w.shape[1] > 1:
            w = w.T
    except Exception:
        return [False] * (N_HYP + 1)

    # H_1: V is a vector space and B is a symmetric bilinear form on V
    try:
        h1 = bool(B.is_square and all(sympy.simplify(B[i, j] - B[j, i]) == 0 
                                      for i in range(B.shape[0]) for j in range(B.shape[1])))
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V, self-adjoint with respect to B
    try:
        diff = B * T - T.T * B
        h2 = bool(T.is_square and T.shape == B.shape and 
                  all(sympy.simplify(x) == 0 for x in diff))
    except Exception:
        h2 = False

    # H_3: \lambda and \mu are distinct eigenvalues of T
    try:
        I = eye(T.shape[0])
        lam_is_eigenval = sympy.simplify((T - lam * I).det()) == 0
        mu_is_eigenval = sympy.simplify((T - mu * I).det()) == 0
        h3 = bool(sympy.simplify(lam - mu) != 0 and lam_is_eigenval and mu_is_eigenval)
    except Exception:
        h3 = False

    # H_4: v and w are eigenvectors of T
    try:
        def is_eigenvector(vec):
            if all(sympy.simplify(x) == 0 for x in vec):
                return False
            T_vec = T * vec
            M = vec.row_join(T_vec)
            # Check if rank of [vec, T_vec] is 1 (all 2x2 minors must be 0)
            for i in range(M.shape[0]):
                for j in range(i + 1, M.shape[0]):
                    det = M[i, 0] * M[j, 1] - M[i, 1] * M[j, 0]
                    if sympy.simplify(det) != 0:
                        return False
            return True

        h4 = bool(
            v.shape == (B.shape[0], 1) and w.shape == (B.shape[0], 1) and
            is_eigenvector(v) and is_eigenvector(w)
        )
    except Exception:
        h4 = False

    # ¬Q: The eigenvectors v and w are not orthogonal with respect to B
    try:
        b_vw = (v.T * B * w)[0, 0]
        neg_q = bool(sympy.simplify(b_vw) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]