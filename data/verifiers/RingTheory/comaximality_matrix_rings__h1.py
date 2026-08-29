import itertools
import math
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I and J are two-sided ideals of R",
    "H_2: I + J = R",
    "H_3: n is a positive integer",
    "¬Q: M_n(I) + M_n(J) != M_n(R)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        # Extract witness components. We expect a finite ring represented by Cayley tables.
        if isinstance(witness, dict):
            R_add = witness.get('R_add')
            R_mul = witness.get('R_mul')
            I = witness.get('I')
            J = witness.get('J')
            n = witness.get('n')
        else:
            R_add = getattr(witness, 'R_add', None)
            R_mul = getattr(witness, 'R_mul', None)
            I = getattr(witness, 'I', None)
            J = getattr(witness, 'J', None)
            n = getattr(witness, 'n', None)
            
        if R_add is None or R_mul is None or I is None or J is None or n is None:
            if isinstance(witness, tuple) and len(witness) == 5:
                R_add, R_mul, I, J, n = witness
            else:
                return [False, False, False, False]
                
        if not isinstance(R_add, (list, tuple)) or not isinstance(R_add[0], (list, tuple)):
            return [False, False, False, False]
            
        m = len(R_add)
        R = list(range(m))
        
        # Find additive identity (zero)
        zero = None
        for i in R:
            if all(R_add[i][j] == j for j in R) and all(R_add[j][i] == j for j in R):
                zero = i
                break
                
        # H_1: I and J are two-sided ideals of R
        def is_ideal(S):
            if not S: 
                return False
            if zero is None or zero not in S: 
                return False
            for a in S:
                for b in S:
                    if R_add[a][b] not in S: 
                        return False
                has_inv = False
                for b in S:
                    if R_add[a][b] == zero and R_add[b][a] == zero:
                        has_inv = True
                        break
                if not has_inv: 
                    return False
                for r in R:
                    if R_mul[a][r] not in S: 
                        return False
                    if R_mul[r][a] not in S: 
                        return False
            return True
            
        try:
            h1 = bool(is_ideal(I) and is_ideal(J))
        except Exception:
            h1 = False
            
        # H_2: I + J = R
        try:
            sums = set()
            for a in I:
                for b in J:
                    sums.add(R_add[a][b])
            h2 = bool(sums == set(R))
        except Exception:
            h2 = False
            
        # H_3: n is a positive integer
        try:
            h3 = bool(isinstance(n, int) and n > 0)
        except Exception:
            h3 = False
            
        # ¬Q: M_n(I) + M_n(J) != M_n(R)
        try:
            def matrix_add(A, B):
                return tuple(tuple(R_add[A[i][j]][B[i][j]] for j in range(n)) for i in range(n))

            def get_matrices(S):
                elements = list(S)
                for rows in itertools.product(elements, repeat=n*n):
                    mat = []
                    for i in range(n):
                        mat.append(tuple(rows[i*n:(i+1)*n]))
                    yield tuple(mat)
                    
            # Prevent memory/time explosion for large n or m
            if h3 and (m**(n*n) <= 300000):
                M_I = list(get_matrices(I))
                M_J = list(get_matrices(J))
                M_R = set(get_matrices(R))
                
                M_I_plus_J = set()
                for A in M_I:
                    for B in M_J:
                        M_I_plus_J.add(matrix_add(A, B))
                        
                q = bool(M_I_plus_J == M_R)
            else:
                # Fallback to component-wise equivalence if matrix generation is too large
                q = bool(sums == set(R))
                
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]