import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sp.MatrixBase):
            return [False, False]
        if not witness.is_square:
            return [False, False]
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        n = witness.shape[0]
        x = sp.Symbol('x')
        p = witness.charpoly(x)
        a = p.all_coeffs()
        
        det_U = witness.det()
        
        conclusion_holds = True
        for j in range(n + 1):
            lhs = a[n - j]
            rhs = ((-1)**n) * det_U * sp.conjugate(a[j])
            diff = sp.simplify(sp.expand(lhs - rhs))
            if diff != 0:
                conclusion_holds = False
                break
                
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a square matrix",
    "¬Q: p(x) != (-x)^n det(U) conjugate(p(1/conjugate(x)))"
]

N_HYP = 1
NEG_Q_INDEX = 1