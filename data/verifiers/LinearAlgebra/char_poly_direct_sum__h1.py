import sympy
from sympy import Matrix, simplify, zeros, eye, expand
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: V = W_1 \\oplus W_2 is a direct sum of two T-invariant subspaces W_1 and W_2",
    "H_3: T_1 and T_2 are the restrictions of T to W_1 and W_2 respectively",
    "¬Q: The characteristic polynomial of T is not the product of the characteristic polynomials of T_1 and T_2"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 5:
            T, W1, W2, T1, T2 = witness
        elif len(witness) == 3:
            T, W1, W2 = witness
            T1, T2 = None, None
        else:
            return [False, False, False, False]
            
        n_rows = T.rows if isinstance(T, Matrix) else 0
        
        def to_matrix(W, n_rows):
            if isinstance(W, list):
                if len(W) == 0:
                    return zeros(n_rows, 0)
                cols = []
                for v in W:
                    if isinstance(v, list):
                        if len(v) > 0 and isinstance(v[0], list):
                            cols.append(Matrix(v))
                        else:
                            cols.append(Matrix(v).reshape(len(v), 1))
                    elif isinstance(v, Matrix):
                        cols.append(v)
                if cols:
                    return Matrix.hstack(*cols)
            return W

        W1 = to_matrix(W1, n_rows)
        W2 = to_matrix(W2, n_rows)
            
        if T1 is None and T2 is None:
            if isinstance(W1, Matrix) and isinstance(W2, Matrix):
                W = W1.row_join(W2)
                if W.is_square and simplify(W.det()) != 0:
                    try:
                        T_W1 = W.LUsolve(T * W1)
                        T_W2 = W.LUsolve(T * W2)
                    except Exception:
                        W_inv = W.inv()
                        T_W1 = W_inv * T * W1
                        T_W2 = W_inv * T * W2
                    k = W1.cols
                    T1 = T_W1[:k, :]
                    T2 = T_W2[k:, :]
                else:
                    T1 = zeros(W1.cols)
                    T2 = zeros(W2.cols)
            else:
                T1 = zeros(0)
                T2 = zeros(0)
    except Exception:
        return [False, False, False, False]

    # H1: T is a linear operator on V
    try:
        h1 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1 = False

    # H2: V = W_1 \oplus W_2 is a direct sum of two T-invariant subspaces W_1 and W_2
    try:
        if not (isinstance(W1, Matrix) and isinstance(W2, Matrix)):
            h2 = False
        else:
            W = W1.row_join(W2)
            is_direct_sum = W.is_square and W.shape == T.shape and simplify(W.det()) != 0
            
            if is_direct_sum:
                k = W1.cols
                try:
                    T_W1 = W.LUsolve(T * W1)
                    T_W2 = W.LUsolve(T * W2)
                except Exception:
                    W_inv = W.inv()
                    T_W1 = W_inv * T * W1
                    T_W2 = W_inv * T * W2
                
                inv1 = all(simplify(T_W1[i, j]) == 0 for i in range(k, W.rows) for j in range(k))
                inv2 = all(simplify(T_W2[i, j]) == 0 for i in range(k) for j in range(W2.cols))
                
                h2 = bool(is_direct_sum and inv1 and inv2)
            else:
                h2 = False
    except Exception:
        h2 = False

    # H3: T_1 and T_2 are the restrictions of T to W_1 and W_2 respectively
    try:
        if not (isinstance(T1, Matrix) and T1.is_square and isinstance(T2, Matrix) and T2.is_square):
            h3 = False
        elif T1.shape[0] != W1.cols or T2.shape[0] != W2.cols:
            h3 = False
        else:
            diff1 = T * W1 - W1 * T1
            res1 = all(simplify(val) == 0 for val in diff1)
            diff2 = T * W2 - W2 * T2
            res2 = all(simplify(val) == 0 for val in diff2)
            h3 = bool(res1 and res2)
    except Exception:
        h3 = False

    # Conclusion: The characteristic polynomial of T is the product of the characteristic polynomials of T_1 and T_2
    try:
        p = T.charpoly(x).as_expr()
        p1 = T1.charpoly(x).as_expr()
        p2 = T2.charpoly(x).as_expr()
        
        concl = simplify(expand(p - p1 * p2)) == 0
        neg_q = not concl
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]