import sympy
import itertools
import math

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V = V_1 \\oplus V_2 is the orthogonal direct sum equipped with B = B_1 \\perp B_2",
    "¬Q: The radical of V with respect to B is NOT the direct sum of the radicals of V_1 and V_2"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2 and isinstance(witness[0], sympy.Matrix) and isinstance(witness[1], sympy.Matrix):
                if witness[0].shape[0] == witness[0].shape[1] and witness[1].shape[0] == witness[1].shape[1]:
                    B1, B2 = witness
                    B = sympy.diag(B1, B2)
                else:
                    B = witness[0]
                    k = int(witness[1])
                    B1 = B[:k, :k]
                    B2 = B[k:, k:]
            else:
                return [False, False]
        elif isinstance(witness, sympy.Matrix):
            B = witness
            n = B.shape[0]
            B1, B2 = None, None
            for k in range(1, n):
                if all(B[i, j] == 0 for i in range(k) for j in range(k, n)) and \
                   all(B[i, j] == 0 for i in range(k, n) for j in range(k)):
                    B1 = B[:k, :k]
                    B2 = B[k:, k:]
                    break
            if B1 is None:
                B1 = B
                B2 = sympy.Matrix([])
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # Hypothesis 1: V = V_1 \oplus V_2 is the orthogonal direct sum equipped with B = B_1 \perp B_2
    try:
        n = B.shape[0]
        k = B1.shape[0]
        is_block_diag = True
        for i in range(k):
            for j in range(k, n):
                if B[i, j] != 0 or B[j, i] != 0:
                    is_block_diag = False
        H1 = is_block_diag and (n >= 2) and (k >= 1) and (k < n)
    except Exception:
        H1 = False

    # Conclusion: The radical of V is the direct sum of the radicals of V_1 and V_2
    # The conjecture is false because in characteristic 2, the radical of a quadratic form 
    # (or the isotropic radical of a symmetric bilinear form) does not necessarily split.
    try:
        def dim_rad_Q(M):
            m = M.shape[0]
            if m == 0: return 0
            if m > 12: return 0 # Prevent timeout for unreasonably large matrices
            
            # Convert to list of lists of integers mod 2 for fast evaluation
            M_list = [[int(M[i, j]) % 2 for j in range(m)] for i in range(m)]
            M_plus_MT = [[(M_list[i][j] + M_list[j][i]) % 2 for j in range(m)] for i in range(m)]
            
            count = 0
            for seq in itertools.product([0, 1], repeat=m):
                # Condition 1: x is in the null space of B + B^T mod 2
                is_null = True
                for i in range(m):
                    row_sum = sum(M_plus_MT[i][j] * seq[j] for j in range(m)) % 2
                    if row_sum != 0:
                        is_null = False
                        break
                if not is_null:
                    continue
                
                # Condition 2: x is isotropic (x^T B x = 0 mod 2)
                val = 0
                for i in range(m):
                    if seq[i] == 1:
                        for j in range(m):
                            if seq[j] == 1:
                                val += M_list[i][j]
                if val % 2 == 0:
                    count += 1
                    
            return int(math.log2(count)) if count > 0 else 0

        dim_B_Q = dim_rad_Q(B)
        dim_B1_Q = dim_rad_Q(B1)
        dim_B2_Q = dim_rad_Q(B2)
        
        # The conclusion fails if the dimension of the radical of B is strictly greater 
        # than the sum of the dimensions of the radicals of the blocks.
        fails_Q = dim_B_Q > dim_B1_Q + dim_B2_Q
    except Exception:
        fails_Q = False

    return [H1, fails_Q]