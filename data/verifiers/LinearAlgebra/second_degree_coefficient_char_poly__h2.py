import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sp.MatrixBase):
            witness = sp.Matrix(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = witness.is_square
    except Exception:
        h1 = False
        
    try:
        n = witness.rows
        x = sp.Symbol('x')
        P = witness.charpoly(x)
        
        # In formal systems like Lean, subtraction on natural numbers is saturating,
        # so n - 2 evaluates to 0 for n < 2. We replicate this behavior to find the 
        # coefficient that the formal statement actually refers to.
        deg = max(0, n - 2)
        c_n_minus_2 = P.nth(deg)
        
        tr_A = witness.trace()
        tr_A2 = (witness**2).trace()
        
        rhs = sp.Rational(1, 2) * (tr_A**2 - tr_A2)
        
        neg_q = bool(sp.simplify(c_n_minus_2 - rhs) != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field of characteristic 0",
    "¬Q: The coefficient c_{n-2} is not equal to 1/2(Tr(A)^2 - Tr(A^2))"
]

N_HYP = 1
NEG_Q_INDEX = 1