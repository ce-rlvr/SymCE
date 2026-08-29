import sympy
from sympy import Matrix, eye, zeros, lcm, gcd

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_diagonalizable_over_Z(M):
    """Check if a matrix is diagonalizable over the integers."""
    if not M.is_square: 
        return False
    try:
        eigenvects = M.eigenvects()
        P_cols = []
        for val, mult, vects in eigenvects:
            if not val.is_integer: 
                return False
            if len(vects) < mult: 
                return False
            for v in vects:
                col = v
                # Clear denominators
                current_lcm = 1
                for i in range(col.rows):
                    _, den = col[i].as_numer_denom()
                    current_lcm = lcm(current_lcm, den)
                col = col * current_lcm
                # Divide by GCD to make primitive
                current_gcd = 0
                for i in range(col.rows):
                    current_gcd = gcd(current_gcd, col[i])
                if current_gcd != 0:
                    col = col / current_gcd
                P_cols.append(col)
        if len(P_cols) != M.rows: 
            return False
        P = Matrix.hstack(*P_cols)
        # A matrix is diagonalizable over Z iff the matrix of primitive eigenvectors is unimodular
        return abs(P.det()) == 1
    except Exception:
        return False

def conditions(witness):
    # 1. Try dictionary duck-typing
    if isinstance(witness, dict):
        try:
            return [bool(witness['h1']), bool(witness['h2']), bool(witness['neg_q'])]
        except KeyError:
            pass

    # 2. Try object with attributes/methods duck-typing
    try:
        h1 = witness.h1() if callable(getattr(witness, 'h1', None)) else witness.h1
        h2 = witness.h2() if callable(getattr(witness, 'h2', None)) else witness.h2
        neg_q = witness.neg_q() if callable(getattr(witness, 'neg_q', None)) else witness.neg_q
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        h1 = witness.is_diagonalizable()
        h2 = witness.is_invariant()
        neg_q = not witness.restriction_is_diagonalizable()
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    try:
        T, W = witness
        h1 = T.is_diagonalizable()
        h2 = W.is_invariant(T)
        neg_q = not T.restrict(W).is_diagonalizable()
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 3. Matrix tuple (T, W)
    try:
        T, W = witness
        if not isinstance(T, Matrix):
            T = Matrix(T)
            
        if not isinstance(W, Matrix):
            try:
                if isinstance(W, list) and all(isinstance(w, Matrix) for w in W):
                    W_mat = Matrix.hstack(*W)
                else:
                    W_mat = Matrix(W)
            except Exception:
                W_mat = Matrix(W)
        else:
            W_mat = W
            
        h1 = T.is_diagonalizable()
        
        rank_W = W_mat.rank()
        aug = Matrix.hstack(W_mat, T * W_mat)
        h2 = (aug.rank() == rank_W)
        
        if not h2:
            neg_q = False
        else:
            basis = W_mat.columnspace()
            if not basis:
                neg_q = False
            else:
                B = Matrix.hstack(*basis)
                T_B = T * B
                A_cols = []
                for i in range(T_B.cols):
                    sol, _ = B.gauss_jordan_solve(T_B[:, i])
                    A_cols.append(sol)
                A = Matrix.hstack(*A_cols)
                
                # Check diagonalizability over C (default)
                neg_q = not A.is_diagonalizable()
                
                # If the matrices are purely integer, the counterexample might be over Z
                if not neg_q and all(x.is_integer for x in T) and all(x.is_integer for x in W_mat):
                    if is_diagonalizable_over_Z(T):
                        h1 = True
                        neg_q = not is_diagonalizable_over_Z(A)
                        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: T is a diagonalizable linear operator on V",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: The restriction operator T|_W is not a diagonalizable operator on W"
]

N_HYP = 2
NEG_Q_INDEX = 2