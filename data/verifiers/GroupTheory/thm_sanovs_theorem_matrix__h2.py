import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
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
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a 2x2 matrix A in SL(2, Z).
    """
    # H_1: A is in SL(2, Z)
    h1_ok = False
    try:
        if isinstance(witness, Matrix) and witness.shape == (2, 2):
            is_int = all(witness[i].is_integer for i in range(4))
            if is_int and witness.det() == 1:
                h1_ok = True
    except Exception:
        h1_ok = False
        
    # neg_Q: H is not isomorphic to the free group of rank 2
    # This is true if and only if there is a non-trivial relation between A and B.
    neg_q_ok = False
    try:
        if h1_ok:
            A = witness
            B = Matrix([[1, 0], [2, 1]])
            
            def to_tuple(M):
                return (int(M[0,0]), int(M[0,1]), int(M[1,0]), int(M[1,1]))
            
            A_inv = A.inv()
            B_inv = B.inv()
            
            matrices_tup = [to_tuple(A), to_tuple(A_inv), to_tuple(B), to_tuple(B_inv)]
            I_tup = (1, 0, 0, 1)
            minus_I_tup = (-1, 0, 0, -1)
            
            # If any generator is I or -I, there is a trivial relation
            if matrices_tup[0] in (I_tup, minus_I_tup) or matrices_tup[2] in (I_tup, minus_I_tup):
                neg_q_ok = True
            else:
                # Iterative Deepening DFS to find the shortest non-trivial relation
                def dfs(last_idx, mat, length, max_l):
                    if length == max_l:
                        # If the word evaluates to I or -I, we found a relation
                        if mat == I_tup or mat == minus_I_tup:
                            return True
                        return False
                    
                    for i in range(4):
                        # Skip the inverse of the last multiplied generator to ensure reduced words
                        if i == (last_idx ^ 1):
                            continue
                        
                        M = matrices_tup[i]
                        next_mat = (
                            mat[0]*M[0] + mat[1]*M[2],
                            mat[0]*M[1] + mat[1]*M[3],
                            mat[2]*M[0] + mat[3]*M[2],
                            mat[2]*M[1] + mat[3]*M[3]
                        )
                        
                        if dfs(i, next_mat, length + 1, max_l):
                            return True
                    return False

                found_relation = False
                # Search for relations up to length 11
                for max_l in range(1, 12):
                    for i in range(4):
                        if dfs(i, matrices_tup[i], 1, max_l):
                            found_relation = True
                            break
                    if found_relation:
                        break
                
                neg_q_ok = found_relation
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is in SL(2, Z)",
    "¬Q: H is not isomorphic to the free group of rank 2"
]

N_HYP = 1
NEG_Q_INDEX = 1