import sympy
from sympy import Matrix, Symbol, eye, zeros, Rational, Integer
from sympy import QQ, RR, CC

# Setup named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def in_F(e, F):
    try:
        if hasattr(F, '__contains__'):
            return e in F
        return False
    except Exception:
        return False

def same_rcf(A, B):
    if A.shape != B.shape:
        return False
    x = Symbol('x')
    try:
        cpA = A.charpoly(x).as_expr().expand()
        cpB = B.charpoly(x).as_expr().expand()
        if cpA != cpB:
            return False
    except Exception:
        return False

    try:
        mpA = A.minimal_polynomial(x).expand()
        mpB = B.minimal_polynomial(x).expand()
        if mpA != mpB:
            return False
    except Exception:
        pass

    if A.shape[0] <= 3:
        return True

    try:
        if hasattr(A, 'is_similar'):
            return A.is_similar(B)
    except Exception:
        pass

    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            n = witness.get('n')
            A = witness.get('A')
            B = witness.get('B')
        else:
            F, n, A, B = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif F in [QQ, RR, CC]:
            h1 = True
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H_3: B is a matrix in GL_n(F)
    try:
        h3 = False
        if isinstance(B, Matrix) and B.shape == (n, n):
            elements_in_F = all(in_F(e, F) for e in B)
            if elements_in_F and B.det() != 0:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: A and B have the same rational canonical form but are not conjugate in GL_n(F)
    try:
        neg_q = False
        if isinstance(A, Matrix) and A.shape == (n, n):
            rcf_same = same_rcf(A, B)
            a_in_f = all(in_F(e, F) for e in A)
            
            # A and B are conjugate in GL_n(F) iff they have the same RCF and A is a matrix over F.
            # (Since B is in GL_n(F), A having the same RCF implies A is invertible, hence in GL_n(F) if over F).
            p_conjugate = rcf_same and a_in_f
            
            # The conclusion is: p_conjugate == rcf_same
            # We want the negation: p_conjugate != rcf_same
            neg_q = (p_conjugate != rcf_same)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "H_3: B is a matrix in GL_n(F)",
    "¬Q: A and B have the same rational canonical form but are not conjugate in GL_n(F)"
]

N_HYP = 3
NEG_Q_INDEX = 3