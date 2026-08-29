import z3
from sympy import Matrix, I, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        B1, B2 = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(B1, Matrix) and isinstance(B2, Matrix) and B1.is_square and B2.is_square and B1.shape == B2.shape
    except Exception:
        h1 = False
        
    try:
        h2 = B1.rank() == B2.rank()
    except Exception:
        h2 = False
        
    try:
        # Check if B1 and B2 are isometric (congruent) over C.
        # We want neg_Q to be True if they are NOT isometric.
        
        # First, check invariants: ranks of symmetric and alternating parts must match.
        sym_rank1 = (B1 + B1.T).rank()
        sym_rank2 = (B2 + B2.T).rank()
        alt_rank1 = (B1 - B1.T).rank()
        alt_rank2 = (B2 - B2.T).rank()
        
        if sym_rank1 != sym_rank2 or alt_rank1 != alt_rank2:
            neg_q = True
        else:
            n = B1.shape[0]
            if n > 3:
                # For matrices larger than 3x3, if invariants match we conservatively return False
                # to avoid z3 timeouts, meaning we cannot confirm they are not isometric.
                neg_q = False
            else:
                solver = z3.Solver()
                P_re = [[z3.Real(f"P_re_{i}_{j}") for j in range(n)] for i in range(n)]
                P_im = [[z3.Real(f"P_im_{i}_{j}") for j in range(n)] for i in range(n)]
                
                def c_mul(u, v):
                    return (u[0]*v[0] - u[1]*v[1], u[0]*v[1] + u[1]*v[0])
                def c_add(u, v):
                    return (u[0]+v[0], u[1]+v[1])
                def c_sub(u, v):
                    return (u[0]-v[0], u[1]-v[1])
                    
                P = [[(P_re[i][j], P_im[i][j]) for j in range(n)] for i in range(n)]
                
                def to_c(val):
                    c = complex(val)
                    return (c.real, c.imag)
                    
                B1_c = [[to_c(B1[i, j]) for j in range(n)] for i in range(n)]
                B2_c = [[to_c(B2[i, j]) for j in range(n)] for i in range(n)]
                
                # Compute B1 * P
                B1_P = [[(0, 0) for j in range(n)] for i in range(n)]
                for i in range(n):
                    for j in range(n):
                        sum_c = (0, 0)
                        for k in range(n):
                            sum_c = c_add(sum_c, c_mul(B1_c[i][k], P[k][j]))
                        B1_P[i][j] = sum_c
                        
                # Compute P^T * (B1 * P)
                PT_B1_P = [[(0, 0) for j in range(n)] for i in range(n)]
                for i in range(n):
                    for j in range(n):
                        sum_c = (0, 0)
                        for k in range(n):
                            sum_c = c_add(sum_c, c_mul(P[k][i], B1_P[k][j]))
                        PT_B1_P[i][j] = sum_c
                        
                # Equate P^T * B1 * P to B2
                for i in range(n):
                    for j in range(n):
                        solver.add(PT_B1_P[i][j][0] == B2_c[i][j][0])
                        solver.add(PT_B1_P[i][j][1] == B2_c[i][j][1])
                        
                # Ensure P is invertible (det(P) != 0)
                if n == 1:
                    det = P[0][0]
                    solver.add(z3.Or(det[0] != 0, det[1] != 0))
                elif n == 2:
                    ad = c_mul(P[0][0], P[1][1])
                    bc = c_mul(P[0][1], P[1][0])
                    det = c_sub(ad, bc)
                    solver.add(z3.Or(det[0] != 0, det[1] != 0))
                elif n == 3:
                    term1 = c_mul(P[0][0], c_sub(c_mul(P[1][1], P[2][2]), c_mul(P[1][2], P[2][1])))
                    term2 = c_mul(P[0][1], c_sub(c_mul(P[1][0], P[2][2]), c_mul(P[1][2], P[2][0])))
                    term3 = c_mul(P[0][2], c_sub(c_mul(P[1][0], P[2][1]), c_mul(P[1][1], P[2][0])))
                    det = c_add(c_sub(term1, term2), term3)
                    solver.add(z3.Or(det[0] != 0, det[1] != 0))
                    
                solver.set("timeout", 2000)
                res = solver.check()
                
                # If unsat, no such invertible P exists, so they are NOT isometric.
                if res == z3.unsat:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over the complex numbers",
    "H_2: rank(B_1) = rank(B_2)",
    "¬Q: B_1 and B_2 are not isometric"
]

N_HYP = 2
NEG_Q_INDEX = 2