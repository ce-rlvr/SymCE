import sympy
from sympy import eye, zeros, Matrix
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            P = witness.get('P', None)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                A, B, P = witness
            elif len(witness) == 2:
                A, B = witness
                P = None
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # Evaluate H_1: There exists an invertible n x n matrix P such that B = P^-1 A P
    try:
        h1 = False
        if hasattr(A, 'rows') and hasattr(A, 'cols') and hasattr(B, 'rows') and hasattr(B, 'cols'):
            if A.rows == A.cols and B.rows == B.cols and A.rows == B.rows:
                n = A.rows
                if P is not None:
                    if hasattr(P, 'rows') and hasattr(P, 'cols') and P.rows == n and P.cols == n:
                        if P.det() != 0:
                            # Check P * B == A * P (equivalent to B == P^-1 * A * P for invertible P)
                            diff_matrix = (P * B - A * P).expand()
                            if diff_matrix == zeros(n, n):
                                h1 = True
                else:
                    # If P is not provided, check if A and B are similar
                    if A.is_similar(B):
                        h1 = True
    except Exception:
        h1 = False

    # Evaluate ¬Q: The characteristic polynomial of A is not equal to the characteristic polynomial of B
    try:
        cp_A = A.charpoly()
        cp_B = B.charpoly()
        diff = (cp_A.as_expr() - cp_B.as_expr()).expand()
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: There exists an invertible n x n matrix P such that B = P^-1 A P",
    "¬Q: The characteristic polynomial of A is not equal to the characteristic polynomial of B"
]

N_HYP = 1
NEG_Q_INDEX = 1