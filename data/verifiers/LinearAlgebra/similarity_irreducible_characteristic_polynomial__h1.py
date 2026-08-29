import sympy
from sympy import Matrix, eye, zeros
import z3

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A and B have the same characteristic polynomial p(x)",
    "H_2: The polynomial p(x) is irreducible over F",
    "¬Q: A and B are not similar over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Unpack witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                A, B, F = witness
            elif len(witness) == 2:
                A, B = witness
                F = sympy.S.Integers
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if not hasattr(A, 'charpoly'):
            A = sympy.Matrix(A)
        if not hasattr(B, 'charpoly'):
            B = sympy.Matrix(B)
            
        x = sympy.Symbol('x')
        pA = A.charpoly(x).as_expr()
        pB = B.charpoly(x).as_expr()
        
        h1 = bool(sympy.simplify(pA - pB) == 0)
    except Exception:
        h1 = False

    # Check H2: p(x) is irreducible over F
    try:
        if F == sympy.S.Integers or str(F) == 'ZZ':
            h2 = sympy.polys.polytools.is_irreducible(pA, domain='ZZ')
        elif F == sympy.S.Reals or str(F) == 'QQ':
            h2 = sympy.polys.polytools.is_irreducible(pA, domain='QQ')
        else:
            h2 = sympy.polys.polytools.is_irreducible(pA, domain=F)
    except Exception:
        h2 = False

    # Check neg_Q: A and B are NOT similar over F
    try:
        n = A.shape[0]
        if A.shape != B.shape or A.shape[0] != A.shape[1]:
            neg_q = True
        else:
            if F == sympy.S.Integers or str(F) == 'ZZ':
                if n == 0:
                    is_similar = True
                    neg_q = not is_similar
                else:
                    solver = z3.Solver()
                    P = [[z3.Int(f'p_{i}_{j}') for j in range(n)] for i in range(n)]
                    
                    # P * A == B * P
                    for i in range(n):
                        for j in range(n):
                            lhs = sum(P[i][k] * int(A[k, j]) for k in range(n))
                            rhs = sum(int(B[i][k]) * P[k][j] for k in range(n))
                            solver.add(lhs == rhs)
                    
                    # Determinant of P must be 1 or -1 for invertibility over ZZ
                    if n == 1:
                        det = P[0][0]
                    elif n == 2:
                        det = P[0][0]*P[1][1] - P[0][1]*P[1][0]
                    elif n == 3:
                        det = (P[0][0]*(P[1][1]*P[2][2] - P[1][2]*P[2][1]) 
                             - P[0][1]*(P[1][0]*P[2][2] - P[1][2]*P[2][0]) 
                             + P[0][2]*(P[1][0]*P[2][1] - P[1][1]*P[2][0]))
                    elif n == 4:
                        det = (P[0][0] * (P[1][1]*(P[2][2]*P[3][3] - P[2][3]*P[3][2]) - P[1][2]*(P[2][1]*P[3][3] - P[2][3]*P[3][1]) + P[1][3]*(P[2][1]*P[3][2] - P[2][2]*P[3][1]))
                             - P[0][1] * (P[1][0]*(P[2][2]*P[3][3] - P[2][3]*P[3][2]) - P[1][2]*(P[2][0]*P[3][3] - P[2][3]*P[3][0]) + P[1][3]*(P[2][0]*P[3][2] - P[2][2]*P[3][0]))
                             + P[0][2] * (P[1][0]*(P[2][1]*P[3][3] - P[2][3]*P[3][1]) - P[1][1]*(P[2][0]*P[3][3] - P[2][3]*P[3][0]) + P[1][3]*(P[2][0]*P[3][1] - P[2][1]*P[3][0]))
                             - P[0][3] * (P[1][0]*(P[2][1]*P[3][2] - P[2][2]*P[3][1]) - P[1][1]*(P[2][0]*P[3][2] - P[2][2]*P[3][0]) + P[1][2]*(P[2][0]*P[3][1] - P[2][1]*P[3][0])))
                    else:
                        raise ValueError("Matrix too large for z3 determinant expansion")
                        
                    solver.add(z3.Or(det == 1, det == -1))
                    is_similar = (solver.check() == z3.sat)
                    neg_q = not is_similar
            else:
                # Over a field (like QQ), SymPy's is_similar checks similarity over the field of fractions
                is_similar = A.is_similar(B)
                neg_q = not is_similar
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]