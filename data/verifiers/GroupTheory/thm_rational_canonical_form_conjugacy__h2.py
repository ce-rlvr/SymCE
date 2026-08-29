import sympy
from sympy import Matrix, Symbol, eye, gcd, Poly
from itertools import combinations

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_matrix(M):
    return hasattr(M, 'rows') and hasattr(M, 'cols') and hasattr(M, 'det') and hasattr(M, 'extract')

def get_invariant_factors(M):
    x = Symbol('x')
    A_poly = x * eye(M.rows) - M
    gcds = []
    for k in range(1, M.rows + 1):
        row_indices = list(combinations(range(M.rows), k))
        col_indices = list(combinations(range(M.cols), k))
        current_gcd = 0
        for rows in row_indices:
            for cols in col_indices:
                sub_M = A_poly.extract(rows, cols)
                d = sub_M.det().expand()
                current_gcd = gcd(current_gcd, d)
                if current_gcd == 1:
                    break
            if current_gcd == 1:
                break
        if current_gcd != 0:
            try:
                p = Poly(current_gcd, x)
                current_gcd = (current_gcd / p.LC()).expand()
            except Exception:
                pass
        gcds.append(current_gcd)
    return gcds

def are_conjugate(A, B):
    try:
        from sympy import solve
        n = A.rows
        P_vars = [Symbol(f'p_{i}_{j}') for i in range(n) for j in range(n)]
        P = Matrix(n, n, P_vars)
        eqs = list(A * P - P * B)
        sol = solve(eqs, P_vars, dict=True)
        if not sol:
            return False
        for s in sol:
            P_sol = P.subs(s)
            det_P = P_sol.det().expand()
            if det_P != 0:
                return True
        return False
    except Exception:
        return A.is_similar(B)

def conditions(witness):
    try:
        if len(witness) == 3:
            F, A, B = witness
        elif len(witness) == 2:
            A, B = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        # In sympy, matrix elements are generally treated as elements of a field (e.g. field of fractions)
        h1 = True
    except Exception:
        h1 = False

    # H2: GL_n(F) is the general linear group of degree n over F
    try:
        # Definitional hypothesis
        h2 = True
    except Exception:
        h2 = False

    # H3: A and B are matrices in GL_n(F)
    try:
        if is_matrix(A) and is_matrix(B):
            if A.rows == A.cols and B.rows == B.cols and A.rows == B.rows:
                h3 = (A.det() != 0) and (B.det() != 0)
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: A and B are conjugate in GL_n(F) if and only if they have the same rational canonical form
    try:
        if not h3:
            neg_q = False
        else:
            conjugate = are_conjugate(A, B)
            try:
                inv_A = get_invariant_factors(A)
                inv_B = get_invariant_factors(B)
                same_rcf = (inv_A == inv_B)
            except Exception:
                same_rcf = A.is_similar(B)
            
            neg_q = not (conjugate == same_rcf)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: GL_n(F) is the general linear group of degree n over F",
    "H_3: A and B are matrices in GL_n(F)",
    "¬Q: Conjugacy in GL_n(F) is not equivalent to having the same rational canonical form"
]

N_HYP = 3
NEG_Q_INDEX = 3