import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        Q = sp.Matrix(witness)
        if not getattr(Q, 'is_square', False):
            H1 = False
        else:
            n = Q.shape[0]
            I = sp.eye(n)
            qtq = sp.simplify(Q.T * Q)
            if qtq != I:
                H1 = False
            else:
                is_real = True
                for cell in Q:
                    if cell.is_real is False:
                        is_real = False
                        break
                H1 = is_real
    except Exception:
        H1 = False

    try:
        Q = sp.Matrix(witness)
        n = Q.shape[0]
        t = sp.Dummy('t')
        p = Q.charpoly(t).as_expr()
        p_inv = p.subs(t, 1/t)
        det_Q = sp.simplify(Q.det())
        rhs = det_Q * (-t)**n * p_inv
        diff = sp.simplify(sp.expand(p - rhs))
        neg_Q = bool(diff != 0)
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: Q is an n x n orthogonal matrix over the real numbers, satisfying Q^T Q = I",
    "¬Q: p_Q(t) != det(Q) * (-t)^n * p_Q(1/t) for some t != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1