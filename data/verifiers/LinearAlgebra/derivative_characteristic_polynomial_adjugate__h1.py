import sympy as sp
from sympy import Symbol, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: p_A(x) = det(xI - A) is the characteristic polynomial of A
    # This implicitly requires that A is a square matrix.
    try:
        if not isinstance(witness, sp.MatrixBase):
            W = sp.Matrix(witness)
        else:
            W = witness
            
        if not W.is_square:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: The formal derivative of p_A(x) with respect to x is NOT equal to 
    # the trace of the adjugate matrix of (xI - A).
    try:
        if not h1:
            neg_q = False
        else:
            if not isinstance(witness, sp.MatrixBase):
                W = sp.Matrix(witness)
            else:
                W = witness
                
            n = W.shape[0]
            I = sp.eye(n)
            
            # M = xI - A
            M = x * I - W
            
            # p_A(x) = det(xI - A)
            p_A = M.det()
            
            # Formal derivative of p_A(x) with respect to x
            deriv = sp.diff(p_A, x)
            
            # Trace of the adjugate matrix of (xI - A)
            adj_M = M.adjugate()
            tr_adj = adj_M.trace()
            
            # Check if they are equal
            diff = sp.simplify(sp.expand(deriv - tr_adj))
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p_A(x) = det(xI - A) is the characteristic polynomial of A",
    "¬Q: The formal derivative of p_A(x) with respect to x is NOT equal to the trace of the adjugate matrix of (xI - A)"
]

N_HYP = 1
NEG_Q_INDEX = 1