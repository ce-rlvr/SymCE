import sympy as sp
from sympy import eye, zeros, Rational

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            B = witness.get('B')
            Q = witness.get('Q')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            B, Q = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: V is a vector space over a field of characteristic not equal to 2
    try:
        h1 = isinstance(B, sp.MatrixBase) and B.is_square
    except Exception:
        h1 = False

    # H_2: B is a symmetric bilinear form on V
    try:
        h2 = bool(h1 and B.is_symmetric())
    except Exception:
        h2 = False

    # neg_Q: B(x,y) = (1/2)(Q(x+y) - Q(x) - Q(y)) FAILS
    try:
        neg_q = False
        if h1:
            if isinstance(Q, sp.MatrixBase) and Q.shape == B.shape:
                neg_q = bool(B != (Q + Q.T) / 2)
            elif callable(Q):
                n = B.shape[0]
                x = sp.Matrix(sp.symbols(f'x0:{n}'))
                y = sp.Matrix(sp.symbols(f'y0:{n}'))
                
                B_xy = sp.expand((x.T * B * y)[0])
                
                Q_x = Q(x)
                if isinstance(Q_x, sp.MatrixBase):
                    Q_x = Q_x[0]
                Q_x = sp.expand(Q_x)
                
                Q_y = Q(y)
                if isinstance(Q_y, sp.MatrixBase):
                    Q_y = Q_y[0]
                Q_y = sp.expand(Q_y)
                
                Q_x_y = Q(x + y)
                if isinstance(Q_x_y, sp.MatrixBase):
                    Q_x_y = Q_x_y[0]
                Q_x_y = sp.expand(Q_x_y)
                
                rhs = sp.expand(Rational(1, 2) * (Q_x_y - Q_x - Q_y))
                diff = sp.simplify(B_xy - rhs)
                neg_q = bool(diff != 0)
            elif isinstance(Q, (int, float, sp.Expr)):
                n = B.shape[0]
                x = sp.Matrix(sp.symbols(f'x0:{n}'))
                y = sp.Matrix(sp.symbols(f'y0:{n}'))
                
                B_xy = sp.expand((x.T * B * y)[0])
                Q_val = sp.sympify(Q)
                
                rhs = sp.expand(Rational(1, 2) * (Q_val - Q_val - Q_val))
                diff = sp.simplify(B_xy - rhs)
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field of characteristic not equal to 2",
    "H_2: B is a symmetric bilinear form on V",
    "¬Q: B(x,y) != (1/2)(Q(x+y) - Q(x) - Q(y)) for some x, y in V"
]

N_HYP = 2
NEG_Q_INDEX = 2