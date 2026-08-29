import sympy
from sympy import Matrix, simplify, Expr

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_scalar(c):
    if isinstance(c, (int, float, complex)):
        return True
    if isinstance(c, Expr) and not getattr(c, 'is_Matrix', False):
        return True
    return False

def is_jordan_matrix(J):
    if not getattr(J, 'is_Matrix', False) or not getattr(J, 'is_square', False):
        return False
    n = J.rows
    if n == 0:
        return True
    i = 0
    while i < n:
        lam = J[i, i]
        k = 1
        while i + k < n and J[i + k - 1, i + k] == 1:
            if J[i + k, i + k] != lam:
                return False
            k += 1
        for r in range(i, i + k):
            for c in range(i, i + k):
                if r == c:
                    if J[r, c] != lam: return False
                elif c == r + 1:
                    if J[r, c] != 1: return False
                else:
                    if J[r, c] != 0: return False
        for r in range(i, i + k):
            for c in range(n):
                if c < i or c >= i + k:
                    if J[r, c] != 0: return False
        i += k
    return True

def conditions(witness):
    A = None
    c = None
    J = None
    
    if isinstance(witness, dict):
        A = witness.get('A')
        c = witness.get('c')
        J = witness.get('J')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 2:
            A, c = witness
        elif len(witness) == 3:
            A, c, J = witness

    # H1: c is a non-zero complex scalar
    try:
        h1 = False
        if c is not None and is_scalar(c):
            if bool(simplify(c) != 0):
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The Jordan canonical form of the matrix cA is NOT obtained by replacing every Jordan block J_k(\lambda) in J with the Jordan block J_k(c\lambda).
    try:
        neg_q = False
        if A is None or c is None:
            neg_q = True
        elif not getattr(A, 'is_Matrix', False):
            neg_q = True
        elif not A.is_square:
            neg_q = True
        else:
            if J is None:
                try:
                    J = A.jordan_form()[1]
                except Exception:
                    pass
            
            if J is None or not is_jordan_matrix(J):
                neg_q = True
            else:
                J_new = J.copy()
                for i in range(J.rows):
                    J_new[i, i] = c * J[i, i]
                
                jcf_cA = (c * A).jordan_form()[1]
                jcf_J_new = J_new.jordan_form()[1]
                if jcf_cA != jcf_J_new:
                    neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: c is a non-zero complex scalar",
    "¬Q: The Jordan canonical form of cA is NOT obtained by replacing every Jordan block J_k(lambda) in J with J_k(c*lambda)"
]

N_HYP = 1
NEG_Q_INDEX = 1