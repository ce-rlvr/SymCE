import sympy
from sympy import eye, zeros
import z3

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, sympy.MatrixBase):
            return [False]
            
        A = witness
        if not A.is_square:
            return [False]
            
        n = A.shape[0]
        
        # Check if A is strictly real
        is_real = True
        for i in range(n):
            for j in range(n):
                try:
                    val = complex(A[i, j])
                    if abs(val.imag) > 1e-9:
                        is_real = False
                        break
                except Exception:
                    # If we cannot convert to complex, assume it's not a simple real number
                    is_real = False
                    break
            if not is_real:
                break
                
        if is_real:
            # The theorem holds unconditionally for all real matrices.
            # Thus, a real matrix cannot be a counterexample.
            return [False]
            
        # If A is not strictly real, it cannot be diagonalizable over R.
        # Thus, the LHS of the equivalence is False.
        lhs = False
        
        # RHS: exists real SPD P such that P A is symmetric
        def exists_real_spd_P(A):
            if n > 4:
                return False
                
            solver = z3.Solver()
            P = [[z3.Real(f"p_{i}_{j}") for j in range(n)] for i in range(n)]
            
            # P is symmetric
            for i in range(n):
                for j in range(i+1, n):
                    solver.add(P[i][j] == P[j][i])
                    
            def det(M):
                if len(M) == 1:
                    return M[0][0]
                if len(M) == 2:
                    return M[0][0]*M[1][1] - M[0][1]*M[1][0]
                if len(M) == 3:
                    return M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1]) - \
                           M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0]) + \
                           M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0])
                if len(M) == 4:
                    res = 0
                    for j in range(4):
                        sub = [[M[r][c] for c in range(4) if c != j] for r in range(1, 4)]
                        res += ((-1)**j) * M[0][j] * det(sub)
                    return res
                raise NotImplementedError
                
            # Sylvester's criterion for positive definiteness
            for k in range(1, n+1):
                sub_P = [[P[i][j] for j in range(k)] for i in range(k)]
                solver.add(det(sub_P) > 0)
                
            A_r = []
            A_i = []
            for i in range(n):
                row_r = []
                row_i = []
                for j in range(n):
                    try:
                        val = complex(A[i, j])
                        row_r.append(val.real)
                        row_i.append(val.imag)
                    except Exception:
                        return False
                A_r.append(row_r)
                A_i.append(row_i)
                
            # P * A is symmetric <=> P * A_r is symmetric AND P * A_i is symmetric
            for i in range(n):
                for j in range(i+1, n):
                    val1 = sum(P[i][k] * A_r[k][j] for k in range(n))
                    val2 = sum(P[j][k] * A_r[k][i] for k in range(n))
                    solver.add(val1 == val2)
                    
                    val3 = sum(P[i][k] * A_i[k][j] for k in range(n))
                    val4 = sum(P[j][k] * A_i[k][i] for k in range(n))
                    solver.add(val3 == val4)
                    
            return solver.check() == z3.sat

        rhs = exists_real_spd_P(A)
        neg_q = (lhs != rhs)
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence between diagonalizability over R and symmetrizability via a real SPD matrix fails"
]

N_HYP = 0
NEG_Q_INDEX = 0