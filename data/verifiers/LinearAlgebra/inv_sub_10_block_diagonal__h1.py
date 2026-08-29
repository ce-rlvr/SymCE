import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Block Diagonal Representation Theorem.
    Witness is expected to be a tuple: (T, U1, U2)
    where T is the linear operator (matrix), and U1, U2 are bases for the subspaces.
    """
    try:
        T_raw, U1_raw, U2_raw = witness
    except Exception:
        return [False, False, False, False]

    # H1: T is a linear operator on V
    try:
        if isinstance(T_raw, list):
            T = Matrix(T_raw)
        else:
            T = T_raw
        h1 = isinstance(T, Matrix) and T.is_square
        if h1:
            n = T.shape[0]
        else:
            n = 0
    except Exception:
        h1 = False

    # Parse U1 and U2 into lists of column vectors
    try:
        def parse_basis(U):
            if isinstance(U, Matrix):
                return [U[:, i] for i in range(U.shape[1])]
            elif isinstance(U, list) or isinstance(U, tuple):
                res = []
                for u in U:
                    if isinstance(u, (list, tuple)):
                        res.append(Matrix(u))
                    elif isinstance(u, Matrix):
                        if u.shape[1] != 1:
                            res.extend([u[:, i] for i in range(u.shape[1])])
                        else:
                            res.append(u)
                return res
            return None

        U1 = parse_basis(U1_raw)
        U2 = parse_basis(U2_raw)
    except Exception:
        U1 = None
        U2 = None

    # H2: V is the direct sum of subspaces U_1 and U_2
    try:
        if not h1 or U1 is None or U2 is None:
            h2 = False
        else:
            valid_U1 = all(u.shape == (n, 1) for u in U1)
            valid_U2 = all(u.shape == (n, 1) for u in U2)
            if not (valid_U1 and valid_U2):
                h2 = False
            else:
                dim_U1 = Matrix.hstack(*U1).rank() if U1 else 0
                dim_U2 = Matrix.hstack(*U2).rank() if U2 else 0
                M = Matrix.hstack(*(U1 + U2)) if (U1 + U2) else Matrix()
                dim_sum = M.rank()
                h2 = (dim_U1 + dim_U2 == n) and (dim_sum == n)
    except Exception:
        h2 = False

    # H3: U_1 and U_2 are both T-invariant
    try:
        if not h1 or not h2:
            h3 = False
        else:
            u1_inv = True
            if U1:
                M1 = Matrix.hstack(*U1)
                rank1 = M1.rank()
                for u in U1:
                    if Matrix.hstack(M1, T * u).rank() > rank1:
                        u1_inv = False
                        break
            
            u2_inv = True
            if U2:
                M2 = Matrix.hstack(*U2)
                rank2 = M2.rank()
                for u in U2:
                    if Matrix.hstack(M2, T * u).rank() > rank2:
                        u2_inv = False
                        break
            
            h3 = u1_inv and u2_inv
    except Exception:
        h3 = False

    # neg_Q: T cannot be represented as a block diagonal matrix with >= 2 blocks
    # This is equivalent to saying T is indecomposable.
    try:
        if not h1:
            neg_q = False
        else:
            if n <= 1:
                neg_q = True
            else:
                # Find the degree of the minimal polynomial
                vecs = [sympy.eye(n).reshape(n * n, 1)]
                deg_min_poly = n
                for k in range(1, n + 1):
                    vecs.append((T**k).reshape(n * n, 1))
                    M = sympy.Matrix.hstack(*vecs)
                    if M.rank() < len(vecs):
                        deg_min_poly = k
                        break
                
                # If degree of minimal polynomial < n, T is decomposable
                if deg_min_poly < n:
                    neg_q = False
                else:
                    # If degree is n, T is indecomposable iff char_poly is a power of an irreducible polynomial
                    sym_x = sympy.Symbol('x')
                    cp = T.charpoly(sym_x).as_expr()
                    factors = sympy.factor_list(cp)
                    if len(factors[1]) > 1:
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: V is the direct sum of subspaces U_1 and U_2",
    "H_3: U_1 and U_2 are both T-invariant",
    "¬Q: There does not exist a basis of V such that the matrix representation of T is a block diagonal matrix (with >= 2 blocks)"
]

N_HYP = 3
NEG_Q_INDEX = 3