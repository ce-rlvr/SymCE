import sympy
from sympy import Matrix, simplify, expand, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Witness is expected to be a tuple: (T, chains)
        # T is a sympy Matrix representing the linear operator.
        # chains is a list of lists/tuples of sympy Matrices representing the Jordan chains.
        T, chains = witness
        
        if not isinstance(T, Matrix) or not T.is_square:
            return [False, False, False, False]
            
        def is_zero_mat(M):
            M = expand(M)
            for i in range(M.rows):
                for j in range(M.cols):
                    if M[i, j] != 0 and simplify(M[i, j]) != 0:
                        return False
            return True

        # H_1: V is a finite-dimensional vector space
        # Implicitly true since T is a finite square matrix.
        h1 = True
        
        eigenvectors = []
        h3 = True
        
        for C in chains:
            if not C:
                h3 = False
                break
            
            # Check if the chain is valid in the forward direction (C[0] is the terminal eigenvector)
            v = C[0]
            lam = None
            for i in range(v.rows):
                val = expand(v[i])
                if val != 0 and simplify(val) != 0:
                    lam = simplify((T * v)[i] / v[i])
                    if is_zero_mat(T * v - lam * v):
                        break
                    else:
                        lam = None
            
            valid_forward = False
            if lam is not None:
                valid_forward = True
                for j in range(1, len(C)):
                    if not is_zero_mat(T * C[j] - lam * C[j] - C[j-1]):
                        valid_forward = False
                        break
            
            if valid_forward:
                eigenvectors.append(v)
                continue
                
            # Check if the chain is valid in the reverse direction (C[-1] is the terminal eigenvector)
            v = C[-1]
            lam = None
            for i in range(v.rows):
                val = expand(v[i])
                if val != 0 and simplify(val) != 0:
                    lam = simplify((T * v)[i] / v[i])
                    if is_zero_mat(T * v - lam * v):
                        break
                    else:
                        lam = None
            
            valid_reverse = False
            if lam is not None:
                valid_reverse = True
                for j in range(len(C)-2, -1, -1):
                    if not is_zero_mat(T * C[j] - lam * C[j] - C[j+1]):
                        valid_reverse = False
                        break
            
            if valid_reverse:
                eigenvectors.append(v)
            else:
                h3 = False
                break
                
        # H_2: v_1, ..., v_p are linearly independent eigenvectors of T
        if not eigenvectors:
            h2 = False
        else:
            E = Matrix.hstack(*eigenvectors)
            h2 = (E.rank() == len(eigenvectors))
            
        # ¬Q: The set of all vectors in the union of the chains is linearly dependent
        all_vectors = []
        for C in chains:
            for v in C:
                is_dup = False
                for u in all_vectors:
                    if is_zero_mat(v - u):
                        is_dup = True
                        break
                if not is_dup:
                    all_vectors.append(v)
                    
        if not all_vectors:
            neg_q = False
        else:
            M = Matrix.hstack(*all_vectors)
            neg_q = (M.rank() < len(all_vectors))
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: v_1, ..., v_p are linearly independent eigenvectors of T",
    "H_3: C_1, ..., C_p are Jordan chains of generalized eigenvectors of T such that the terminal eigenvector of each chain C_i is v_i",
    "¬Q: The set of all vectors in the union of the chains C_1 U ... U C_p is linearly dependent"
]

N_HYP = 3
NEG_Q_INDEX = 3