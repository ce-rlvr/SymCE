import sympy
from sympy import Matrix, eye, zeros
import z3

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B = witness
        A = Matrix(A)
        B = Matrix(B)
    except Exception:
        return [False, False]
        
    # H_1: A and B are real symmetric n x n matrices
    try:
        h1 = False
        if A.is_square and B.is_square and A.shape == B.shape:
            if A == A.T and B == B.T:
                def is_real_num(val):
                    try:
                        float(val)
                        return True
                    except Exception:
                        return False
                if all(is_real_num(e) for e in A) and all(is_real_num(e) for e in B):
                    h1 = True
    except Exception:
        h1 = False
        
    # ¬Q: There does NOT exist a real scalar mu such that A + mu B is positive definite.
    try:
        neg_q = False
        if h1:
            n = A.shape[0]
            mu = z3.Real('mu')
            solver = z3.Solver()
            
            x = sympy.Symbol('x', real=True)
            M = A + x * B
            
            # Sylvester's criterion: a real symmetric matrix is positive definite 
            # iff all its leading principal minors are strictly positive.
            for i in range(1, n + 1):
                minor_matrix = M[:i, :i]
                det_expr = minor_matrix.det()
                poly = sympy.Poly(det_expr, x)
                coeffs = poly.all_coeffs()
                
                z3_expr = 0
                degree = len(coeffs) - 1
                for j, coeff in enumerate(coeffs):
                    if coeff.is_Rational:
                        z3_coeff = z3.RealVal(str(coeff))
                    else:
                        z3_coeff = z3.RealVal(float(coeff))
                        
                    if degree - j == 0:
                        z3_expr += z3_coeff
                    else:
                        z3_expr += z3_coeff * (mu ** (degree - j))
                        
                solver.add(z3_expr > 0)
                
            if solver.check() == z3.unsat:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are real symmetric n x n matrices",
    "¬Q: There does not exist a real scalar mu such that A + mu B is positive definite"
]

N_HYP = 1
NEG_Q_INDEX = 1