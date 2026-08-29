import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is a linear operator on V",
    "H_3: W is a T-invariant subspace of V",
    "¬Q: There does not exist a T-invariant subspace U of V such that V = W ⊕ U"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
            
        T, W = witness
        
        # H1 and H2: T is a linear operator on a finite-dimensional vector space V
        if isinstance(T, Matrix) and T.is_square:
            h1 = True
            h2 = True
            n = T.shape[0]
            
            # Parse W into a basis matrix B
            M = None
            if isinstance(W, list):
                if len(W) == 0:
                    M = zeros(n, 0)
                elif isinstance(W[0], list):
                    M = Matrix(W).T
                elif isinstance(W[0], Matrix):
                    cols = [v.reshape(n, 1) for v in W]
                    M = Matrix.hstack(*cols)
            elif isinstance(W, Matrix):
                M = W
                
            if M is not None and M.shape[0] == n:
                # Extract linearly independent columns to form a basis for W
                _, pivots = M.rref()
                if len(pivots) == 0:
                    B = zeros(n, 0)
                else:
                    B = M[:, pivots]
                
                k = B.shape[1]
                
                # H3: W is a T-invariant subspace of V
                if k == 0:
                    h3 = True
                    neg_q = False
                else:
                    TB = T * B
                    augmented = B.row_join(TB)
                    if augmented.rank() == k:
                        h3 = True
                        
                        # ¬Q: Check if there is NO T-invariant complement U
                        # A complement U is T-invariant iff there exists a projection P onto W commuting with T.
                        # P = B * A for some k x n matrix A such that A * B = I_k and B * A * T = T * B * A.
                        if k == n:
                            neg_q = False
                        else:
                            A_vars = sympy.symbols(f'a_0:{k*n}')
                            A = Matrix(k, n, A_vars)
                            
                            eqs = []
                            
                            # Condition 1: A * B = I_k
                            AB = A * B
                            Ik = eye(k)
                            for i in range(k):
                                for j in range(k):
                                    eqs.append(AB[i, j] - Ik[i, j])
                                    
                            # Condition 2: B * A * T = T * B * A
                            BAT = B * A * T
                            TBA = T * B * A
                            for i in range(n):
                                for j in range(n):
                                    eqs.append(BAT[i, j] - TBA[i, j])
                                    
                            # If the linear system has no solution, no such complement exists
                            sol = sympy.linsolve(eqs, A_vars)
                            if not sol:
                                neg_q = True
                            else:
                                neg_q = False
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]