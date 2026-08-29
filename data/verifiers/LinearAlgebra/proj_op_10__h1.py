import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not getattr(witness, 'is_Matrix', False):
            return [False]
        
        P = witness
        
        # Calculate squared Frobenius norm
        frob_sq = sympy.simplify(sum(P[i, j] * P[i, j].conjugate() for i in range(P.rows) for j in range(P.cols)))
        
        # Calculate rank
        rank_P = P.rank()
        
        # Check if squared Frobenius norm equals rank
        diff = sympy.simplify(frob_sq - rank_P)
        try:
            cond1 = abs(complex(diff)) < 1e-12
        except TypeError:
            cond1 = (diff == 0)
        
        # Check if P is an orthogonal projection
        if P.is_square:
            is_proj = (P**2 == P)
            is_hermitian = (P.H == P)
            cond2 = bool(is_proj and is_hermitian)
        else:
            cond2 = False
            
        # The conclusion is cond1 <=> cond2
        # The negation is cond1 != cond2 (XOR)
        neg_q = (bool(cond1) != cond2)
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: (||P||_F^2 == rank(P)) is not equivalent to (P is an orthogonal projection)"
]

N_HYP = 0
NEG_Q_INDEX = 0