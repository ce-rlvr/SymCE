import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            A, X, Y, lambdas = witness
            n = A.shape[0]
            
            h1 = True
            for i in range(n):
                diff = A * X[i] - lambdas[i] * X[i]
                if not all(simplify(diff[k, 0]) == 0 for k in range(n)):
                    h1 = False
                    break
                    
            h2 = True
            for i in range(n):
                diff = Y[i].T * A - lambdas[i] * Y[i].T
                if not all(simplify(diff[0, k]) == 0 for k in range(n)):
                    h2 = False
                    break
                    
            h3 = True
            for i in range(n):
                for j in range(n):
                    dot = (Y[i].T * X[j])[0, 0]
                    dot_simp = simplify(dot)
                    if i == j:
                        if dot_simp != 1: h3 = False
                    else:
                        if dot_simp != 0: h3 = False
        else:
            A = witness
            is_diag = A.is_diagonalizable()
            h1 = is_diag
            h2 = is_diag
            h3 = is_diag
            
        atoms = [a for a in A.atoms() if a.is_number]
        is_rat = all(a.is_rational for a in atoms) if atoms else False
        is_real = all(a.is_real for a in atoms) if atoms else False
        
        is_diag_F = True
        eigenvals = A.eigenvals()
        for ev, alg_mult in eigenvals.items():
            if is_rat and ev.is_rational is False:
                is_diag_F = False
                break
            if is_real and ev.is_real is False:
                is_diag_F = False
                break
            
            M = A - ev * eye(A.shape[0])
            if len(M.nullspace()) != alg_mult:
                is_diag_F = False
                break
                
        neg_q = not is_diag_F

    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: There exists a set of n right column eigenvectors {x_1, ..., x_n} of A such that A x_i = \\lambda_i x_i",
    "H_2: There exists a set of n left column eigenvectors {y_1, ..., y_n} of A such that y_i^T A = \\lambda_i y_i^T",
    "H_3: The dot product y_i^T x_j = \\delta_{ij} (the Kronecker delta) for all 1 <= i, j <= n",
    "¬Q: The matrix A is not diagonalizable over F"
]

N_HYP = 3
NEG_Q_INDEX = 3