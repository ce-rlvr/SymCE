import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Witness is expected to be a tuple: (L_basis, S, x_mat)
    where:
      - L_basis: list of n x n SymPy matrices forming a basis for the field L over K (K is implicitly scalar matrices).
      - S: n x n SymPy matrix representing the generator sigma of Gal(L/K) via conjugation (sigma(M) = S * M * S^{-1}).
      - x_mat: n x n SymPy matrix representing the element x.
    """
    try:
        L_basis, S, x_mat = witness
    except Exception:
        return [False, False, False]

    def check_h1():
        try:
            n = len(L_basis)
            if n < 2: 
                return False
            for B in L_basis:
                if not isinstance(B, Matrix): 
                    return False
                if B.shape != (n, n): 
                    return False
            
            # Check if L_basis is of the form [I, M, M^2, ..., M^{n-1}]
            if L_basis[0] != eye(n): 
                return False
            
            M = L_basis[1]
            # M must generate a field extension of degree n over QQ
            if not M.charpoly().is_irreducible(): 
                return False
            
            for i in range(n):
                if L_basis[i] != M**i: 
                    return False
                
            return True
        except Exception:
            return False

    def check_h2():
        try:
            n = len(L_basis)
            S_inv = S.inv()
            M = L_basis[1]
            
            # sigma(M) must be in L. Since L is the centralizer of M, sigma(M) must commute with M.
            sigma_M = S * M * S_inv
            if sigma_M * M != M * sigma_M: 
                return False
            
            # Check that the order of sigma is exactly n
            curr = M
            for k in range(1, n):
                curr = S * curr * S_inv
                if curr == M: 
                    return False
                
            curr = S * curr * S_inv
            if curr != M: 
                return False
            
            return True
        except Exception:
            return False

    def check_neg_q():
        try:
            n = len(L_basis)
            S_inv = S.inv()
            
            # LHS: Tr(x) == 0
            lhs = (x_mat.trace() == 0)
            
            # RHS: exists y in L such that x == y - sigma(y)
            def flatten(mat):
                return [mat[i, j] for i in range(n) for j in range(n)]
                
            vectors = []
            for B in L_basis:
                diff = B - S * B * S_inv
                vectors.append(flatten(diff))
                
            # Check if x_mat is in the span of { y - sigma(y) | y in L }
            V = Matrix(vectors).T
            rank_V = V.rank()
            
            V_aug = Matrix(vectors + [flatten(x_mat)]).T
            rank_V_aug = V_aug.rank()
            
            rhs = (rank_V == rank_V_aug)
            
            # The conclusion is LHS iff RHS
            Q = (lhs == rhs)
            
            # We want the conclusion to FAIL
            return not Q
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: L/K is a finite cyclic Galois extension",
    "H_2: sigma is a generator of the Galois group Gal(L/K)",
    "¬Q: The conclusion 'Tr_{L/K}(x) = 0 iff exists y in L such that x = y - sigma(y)' fails"
]

N_HYP = 2
NEG_Q_INDEX = 2