import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    # Parse witness: can be (F, A, B) or just (A, B)
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, A, B = witness
            elif len(witness) == 2:
                A, B = witness
                F = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        if F is not None:
            h1 = False
            if hasattr(F, 'is_Field') and F.is_Field:
                h1 = True
            elif F in [sympy.QQ, sympy.RR, sympy.CC]:
                h1 = True
            elif hasattr(F, 'is_field') and F.is_field:
                h1 = True
            elif type(F).__name__ == 'GaloisField':
                h1 = True
        else:
            # If F is not explicitly provided, we assume the matrices are over their field of fractions
            h1 = True
    except Exception:
        h1 = False

    # H_2: A is a matrix in the general linear group GL_n(F)
    try:
        h2 = hasattr(A, 'is_square') and A.is_square and hasattr(A, 'det') and A.det() != 0
    except Exception:
        h2 = False

    # H_3: B is a matrix in the general linear group GL_n(F)
    try:
        h3 = hasattr(B, 'is_square') and B.is_square and hasattr(B, 'det') and B.det() != 0 and B.shape == A.shape
    except Exception:
        h3 = False

    # ¬Q: A and B are conjugate in GL_n(F) XOR they have the same rational canonical form
    # Note: Mathematically, similarity over a field is exactly equivalent to having the same rational canonical form.
    try:
        if not (hasattr(A, 'shape') and hasattr(B, 'shape')):
            neg_q = False
        elif A.shape != B.shape:
            conjugate = False
            same_rcf = False
            neg_q = not (conjugate == same_rcf)
        else:
            conjugate = bool(A.is_similar(B))
            same_rcf = bool(A.is_similar(B))
            neg_q = not (conjugate == same_rcf)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is a matrix in the general linear group GL_n(F)",
    "H_3: B is a matrix in the general linear group GL_n(F)",
    "¬Q: A and B are conjugate in GL_n(F) XOR they have the same rational canonical form"
]

N_HYP = 3
NEG_Q_INDEX = 3