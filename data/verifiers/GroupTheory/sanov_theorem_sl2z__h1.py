import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is in SL(2, Z)
    try:
        if not isinstance(witness, Matrix):
            h1 = False
        elif witness.shape != (2, 2):
            h1 = False
        else:
            h1 = True
            for val in witness:
                if not val.is_integer:
                    h1 = False
                    break
            if h1:
                h1 = (witness.det() == 1)
    except Exception:
        h1 = False

    # ¬Q: H is not isomorphic to the free group of rank 2
    # This is true if there is any non-trivial relation between A and B.
    try:
        A_mat = witness
        B_mat = Matrix([[1, 0], [2, 1]])
        
        A_inv_mat = A_mat.inv()
        B_inv_mat = B_mat.inv()
        
        def mat_to_tuple(M):
            for val in M:
                if not val.is_integer:
                    raise ValueError("Not integer")
            return (int(M[0,0]), int(M[0,1]), int(M[1,0]), int(M[1,1]))
            
        A = mat_to_tuple(A_mat)
        B = mat_to_tuple(B_mat)
        A_inv = mat_to_tuple(A_inv_mat)
        B_inv = mat_to_tuple(B_inv_mat)
        I = (1, 0, 0, 1)
        
        gens = [A, B, A_inv, B_inv]
        inverses = {0: 2, 1: 3, 2: 0, 3: 1}
        
        def mul(M1, M2):
            return (
                M1[0]*M2[0] + M1[1]*M2[2], M1[0]*M2[1] + M1[1]*M2[3],
                M1[2]*M2[0] + M1[3]*M2[2], M1[2]*M2[1] + M1[3]*M2[3]
            )
            
        neg_q = False
        
        # Check length 1 relations
        for i in range(4):
            if gens[i] == I:
                neg_q = True
                break
                
        # BFS to find any relation up to length 12
        if not neg_q:
            queue = [(gens[i], i) for i in range(4)]
            max_len = 12
            for length in range(2, max_len + 1):
                next_queue = []
                for mat, last_idx in queue:
                    for i in range(4):
                        if i != inverses[last_idx]:
                            new_mat = mul(mat, gens[i])
                            if new_mat == I:
                                neg_q = True
                                break
                            next_queue.append((new_mat, i))
                    if neg_q:
                        break
                if neg_q:
                    break
                queue = next_queue
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is in SL(2, Z)",
    "¬Q: H is not isomorphic to the free group of rank 2"
]

N_HYP = 1
NEG_Q_INDEX = 1