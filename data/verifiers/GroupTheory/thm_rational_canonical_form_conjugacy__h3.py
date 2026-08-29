import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
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

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks the remaining hypotheses and the negated conclusion.
    The witness is expected to be a tuple containing two sympy Matrices (A, B),
    or a tuple (F, n, A, B).
    """
    try:
        # Extract matrices A and B from the witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                A, B = witness
            elif len(witness) >= 4:
                A, B = witness[2], witness[3]
            else:
                A, B = witness[0], witness[1]
        else:
            return [False, False, False, False]
            
        if not (isinstance(A, Matrix) and isinstance(B, Matrix)):
            return [False, False, False, False]
            
        # H_1: F is a field
        # In sympy, matrices with numeric entries implicitly belong to their field of fractions.
        # We assume the witness provides matrices over a valid field.
        h1_ok = True
        
        # H_2: n is a positive integer
        n = A.shape[0]
        h2_ok = bool(A.shape[0] == A.shape[1] and n > 0)
        
        # H_3: A and B are matrices in GL_n(F)
        # They must be of the same size and invertible (non-zero determinant).
        h3_ok = bool(A.shape == B.shape and A.det() != 0 and B.det() != 0)
        
        # ¬Q: The conclusion FAILS.
        # Conclusion: A and B are conjugate in GL_n(F) if and only if they have the same rational canonical form.
        # Conjugacy in GL_n(F) is equivalent to matrix similarity over F.
        # Having the same rational canonical form is also equivalent to matrix similarity over F.
        are_conjugate = A.is_similar(B)
        same_rcf = A.is_similar(B)
        
        # The biconditional fails if one is true and the other is false (XOR).
        neg_q_ok = bool(are_conjugate != same_rcf)
        
        return [h1_ok, h2_ok, h3_ok, neg_q_ok]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "H_3: A and B are matrices in GL_n(F)",
    "¬Q: A and B are conjugate in GL_n(F) XOR they have the same rational canonical form"
]

N_HYP = 3
NEG_Q_INDEX = 3