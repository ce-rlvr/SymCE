import sympy
import sympy.matrices
from sympy import Symbol, Integer, eye, zeros
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is a square matrix of size n >= 2
    try:
        if not isinstance(witness, sympy.matrices.MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            n = witness.shape[0]
            h1 = n >= 2
    except Exception:
        h1 = False

    # H_2: p_0(x) = 1 and p_1(x) = x - a_1
    try:
        if h1:
            a_1 = witness[0, 0]
            p_1 = witness[:1, :1].charpoly(x).as_expr()
            diff = sympy.expand(p_1 - (x - a_1))
            h2 = (diff == 0) or (sympy.simplify(diff) == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The recurrence relation fails for some 2 <= k <= n
    try:
        if h1:
            neg_q = False
            def p(k):
                if k == 0:
                    return Integer(1)
                else:
                    return witness[:k, :k].charpoly(x).as_expr()
            
            for k in range(2, n + 1):
                a_k = witness[k-1, k-1]
                b_k_minus_1 = witness[k-1, k-2]
                c_k_minus_1 = witness[k-2, k-1]
                
                lhs = p(k)
                rhs = (x - a_k) * p(k-1) - b_k_minus_1 * c_k_minus_1 * p(k-2)
                
                diff = sympy.expand(lhs - rhs)
                if diff != 0 and sympy.simplify(diff) != 0:
                    neg_q = True
                    break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square matrix of size n >= 2",
    "H_2: p_0(x) = 1 and p_1(x) = x - a_1",
    "¬Q: The recurrence relation fails for some 2 <= k <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2