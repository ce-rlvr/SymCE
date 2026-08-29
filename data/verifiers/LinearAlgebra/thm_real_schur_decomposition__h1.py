import sympy as sp
import z3
import math
import itertools
import functools

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "¬Q: There does not exist a real orthogonal matrix Q such that Q^T A Q is a block upper triangular matrix with 1x1 and 2x2 diagonal blocks"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if not isinstance(witness, sp.MatrixBase):
            witness = sp.Matrix(witness)
            
        if witness.rows != witness.cols:
            return [False]
            
        n = witness.rows
        
        # For 1x1 and 2x2 matrices, the matrix itself is trivially a block upper triangular 
        # matrix with 1x1 and 2x2 blocks. Thus, Q = I works and the conclusion holds.
        if n <= 2:
            return [False]
            
        B_sympy = sp.re(witness)
        C_sympy = sp.im(witness)
        
        def sympy_to_z3_real(val):
            if val.is_Integer:
                return z3.RealVal(int(val))
            elif val.is_Rational:
                return z3.RealVal(f"{val.p}/{val.q}")
            elif val.is_Float:
                return z3.RealVal(float(val))
            else:
                val_simp = sp.simplify(val)
                if val_simp.is_Integer:
                    return z3.RealVal(int(val_simp))
                elif val_simp.is_Rational:
                    return z3.RealVal(f"{val_simp.p}/{val_simp.q}")
                else:
                    val_real = sp.re(val_simp).evalf()
                    return z3.RealVal(float(val_real))
                    
        B = [[sympy_to_z3_real(B_sympy[i, j]) for j in range(n)] for i in range(n)]
        C = [[sympy_to_z3_real(C_sympy[i, j]) for j in range(n)] for i in range(n)]
        
        if n == 3:
            # For n=3, the blocks must be (1, 2), (2, 1), or (1, 1, 1).
            # This is equivalent to Re(A) and Im(A) sharing a real eigenvector, 
            # OR Re(A^T) and Im(A^T) sharing a real eigenvector.
            def share_real_eigenvector(Mat1, Mat2):
                solver = z3.Solver()
                x = [z3.Real(f'x_{i}') for i in range(n)]
                lam = z3.Real('lam')
                mu = z3.Real('mu')
                
                solver.add(sum(x[i]*x[i] for i in range(n)) == 1)
                for i in range(n):
                    bx = sum(Mat1[i][j] * x[j] for j in range(n))
                    cx = sum(Mat2[i][j] * x[j] for j in range(n))
                    solver.add(bx == lam * x[i])
                    solver.add(cx == mu * x[i])
                
                solver.set("timeout", 2000)
                res = solver.check()
                if res == z3.sat:
                    return True
                elif res == z3.unsat:
                    return False
                else:
                    return True # Fallback to True to avoid false positives on timeout
                    
            B_T = [[B[j][i] for j in range(n)] for i in range(n)]
            C_T = [[C[j][i] for j in range(n)] for i in range(n)]
            
            has_1_2 = share_real_eigenvector(B, C)
            has_2_1 = share_real_eigenvector(B_T, C_T)
            
            conclusion_holds = has_1_2 or has_2_1
            return [not conclusion_holds]
            
        else:
            # General formulation for n >= 4
            solver = z3.Solver()
            Q = [[z3.Real(f'q_{i}_{j}') for j in range(n)] for i in range(n)]
            
            # Q is orthogonal
            for i in range(n):
                for j in range(i, n):
                    dot = sum(Q[k][i] * Q[k][j] for k in range(n))
                    if i == j:
                        solver.add(dot == 1)
                    else:
                        solver.add(dot == 0)
                        
            def get_M(Mat, i, j):
                return sum(Q[k][i] * Mat[k][l] * Q[l][j] for k in range(n) for l in range(n))
                
            # Zeros below the first subdiagonal
            for i in range(n):
                for j in range(n):
                    if i > j + 1:
                        solver.add(get_M(B, i, j) == 0)
                        solver.add(get_M(C, i, j) == 0)
                        
            # No two consecutive non-zero subdiagonal elements (forces blocks to be <= 2x2)
            for k in range(n - 2):
                mb1 = get_M(B, k+1, k)
                mc1 = get_M(C, k+1, k)
                mb2 = get_M(B, k+2, k+1)
                mc2 = get_M(C, k+2, k+1)
                solver.add(z3.Or(
                    z3.And(mb1 == 0, mc1 == 0),
                    z3.And(mb2 == 0, mc2 == 0)
                ))
                
            solver.set("timeout", 4000)
            res = solver.check()
            if res == z3.sat:
                conclusion_holds = True
            elif res == z3.unsat:
                conclusion_holds = False
            else:
                conclusion_holds = True # Fallback to True to avoid false positives on timeout
                
            return [not conclusion_holds]
            
    except Exception:
        return [False]