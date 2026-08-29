import sympy
from sympy import Matrix, zeros, I, eye

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        vectors, G = witness
    except Exception:
        return [False, False, False]

    # H_1: v_1, ..., v_n is a finite sequence of vectors in V
    try:
        H_1 = isinstance(vectors, (list, tuple)) and len(vectors) > 0
        if H_1:
            H_1 = all(isinstance(v, Matrix) for v in vectors)
        if H_1:
            shape = vectors[0].shape
            H_1 = all(v.shape == shape for v in vectors) and shape[1] == 1
    except Exception:
        H_1 = False

    # H_2: G is the n x n Gram matrix defined by G_{ij} = <v_i, v_j>
    try:
        n = len(vectors)
        H_2 = isinstance(G, Matrix) and G.shape == (n, n)
        if H_2:
            G1 = zeros(n, n)
            G2 = zeros(n, n)
            for i in range(n):
                for j in range(n):
                    # vdot computes the inner product (conjugate-linear in the first argument in sympy)
                    G1[i, j] = vectors[i].vdot(vectors[j])
                    G2[i, j] = vectors[j].vdot(vectors[i])
            
            diff1 = G - G1
            diff2 = G - G2
            if diff1.is_zero_matrix == True or diff2.is_zero_matrix == True:
                H_2 = True
            else:
                H_2 = (sympy.simplify(diff1).is_zero_matrix == True) or (sympy.simplify(diff2).is_zero_matrix == True)
    except Exception:
        H_2 = False

    # neg_Q: The matrix G is symmetric and positive semidefinite, and it is positive definite if and only if the vectors v_1, ..., v_n are linearly independent.
    try:
        diff_sym = G - G.T
        is_sym = (diff_sym.is_zero_matrix == True)
        if not is_sym:
            is_sym = (sympy.simplify(diff_sym).is_zero_matrix == True)
            
        if not is_sym:
            conclusion = False
        else:
            evals = G.eigenvals()
            is_psd = True
            is_pd = True
            for e in evals.keys():
                try:
                    c = complex(e)
                    if abs(c.imag) > 1e-7:
                        is_psd = False
                        is_pd = False
                        break
                    if c.real < -1e-7:
                        is_psd = False
                    if c.real <= 1e-7:
                        is_pd = False
                except TypeError:
                    if e.is_real is False:
                        is_psd = False
                        is_pd = False
                        break
                    if e.is_nonnegative is False:
                        is_psd = False
                    if e.is_positive is False:
                        is_pd = False
            
            M = Matrix.hstack(*vectors)
            is_lin_indep = (M.rank() == len(vectors))
            
            conclusion = is_psd and (is_pd == is_lin_indep)
            
        neg_Q = not conclusion
    except Exception:
        neg_Q = False

    return [bool(H_1), bool(H_2), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: v_1, ..., v_n is a finite sequence of vectors in V",
    "H_2: G is the n x n Gram matrix defined by G_{ij} = <v_i, v_j>",
    "¬Q: G is not symmetric, not positive semidefinite, or its positive definiteness does not match the linear independence of the vectors"
]

N_HYP = 2
NEG_Q_INDEX = 2