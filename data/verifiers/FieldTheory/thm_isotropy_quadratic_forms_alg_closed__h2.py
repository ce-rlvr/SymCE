import sympy
from sympy import Matrix, eye, zeros, Expr, Poly

I1 = eye(1)
I2 = eye(2)
I3 = eye(3)
O1 = zeros(1, 1)
O2 = zeros(2, 2)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            field, mat = witness
        else:
            mat = witness
            
        if isinstance(mat, list):
            mat = Matrix(mat)
            
        if isinstance(mat, Matrix):
            h1 = all(e.is_number for e in mat)
            h2 = mat.is_square and mat.is_symmetric()
            
            if h1 and h2:
                n = mat.shape[0]
                if n == 0:
                    neg_q = True
                elif n == 1:
                    neg_q = not mat[0, 0].is_zero
                else:
                    neg_q = False
                    
        elif isinstance(mat, Expr):
            free_symbols = list(mat.free_symbols)
            if free_symbols:
                poly = Poly(mat, free_symbols)
                if poly.is_homogeneous and poly.total_degree() == 2:
                    h1 = True
                    h2 = True
                    if len(free_symbols) == 1:
                        a = poly.coeff_monomial(free_symbols[0]**2)
                        neg_q = not a.is_zero
                    else:
                        neg_q = False
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: q: V \\to K is a quadratic form",
    "¬Q: There does not exist a non-zero vector v \\in V such that q(v) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2