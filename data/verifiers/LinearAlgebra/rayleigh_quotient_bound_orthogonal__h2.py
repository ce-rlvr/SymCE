import sympy as sp
from sympy import Matrix, eye, simplify, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            Q = witness.get('Q')
            x = witness.get('x')
        elif isinstance(witness, tuple) and len(witness) == 2:
            Q, x = witness
        else:
            Q = witness
            x = None
    except Exception:
        return [False, False]

    # H_1: Q is an n x n real orthogonal matrix
    h1 = False
    n = 0
    try:
        if isinstance(Q, (list, tuple)):
            Q = Matrix(Q)
        if isinstance(Q, Matrix) and Q.rows == Q.cols and Q.rows > 0:
            n = Q.rows
            if all(getattr(e, 'is_real', False) for e in Q):
                if simplify(Q.T * Q - eye(n)).is_zero_matrix:
                    h1 = True
    except Exception:
        pass

    # neg_Q: The ratio does not satisfy -1 <= ratio <= 1
    neg_q = False
    try:
        if x is None:
            # If x is not provided, we test with the zero vector, 
            # which is a valid counterexample if the "non-zero" hypothesis was dropped.
            x = zeros(n, 1)
            
        if isinstance(x, (list, tuple)):
            x = Matrix(x)
        if isinstance(x, Matrix):
            if x.rows == 1 and x.cols == n:
                x = x.T
            if x.cols == 1 and x.rows == n:
                num = (x.T * Q * x)[0, 0]
                den = (x.T * x)[0, 0]
                
                den_simp = simplify(den)
                if den_simp == 0:
                    neg_q = True
                else:
                    ratio = simplify(num / den_simp)
                    if ratio.is_real is False:
                        neg_q = True
                    elif ratio.is_real:
                        if not (bool(ratio >= -1) and bool(ratio <= 1)):
                            neg_q = True
                    else:
                        ratio_f = ratio.evalf()
                        if ratio_f.is_real is False:
                            neg_q = True
                        elif not (bool(ratio_f >= -1) and bool(ratio_f <= 1)):
                            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real orthogonal matrix",
    "¬Q: The ratio x^T Q x / x^T x does not satisfy -1 <= ratio <= 1"
]

N_HYP = 1
NEG_Q_INDEX = 1