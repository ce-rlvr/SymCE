import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix, eye, zeros

# Top-level setup
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
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, Matrix):
            n_rows, n_cols = witness.shape
            h1_ok = (n_rows == n_cols and n_rows >= 0)
            h2_ok = True
            neg_q_ok = abs(witness.det()) != 1
        elif isinstance(witness, int):
            h1_ok = witness >= 0
            h2_ok = True
            neg_q_ok = False
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, phi = witness
            h1_ok = isinstance(n, int) and n >= 0
            h2_ok = True
            if isinstance(phi, Matrix):
                neg_q_ok = abs(phi.det()) != 1
            elif hasattr(phi, 'is_surjective'):
                neg_q_ok = not phi.is_surjective
            else:
                neg_q_ok = False
        elif hasattr(witness, 'is_surjective'):
            h1_ok = True
            h2_ok = True
            neg_q_ok = not witness.is_surjective
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let F_n be a free group of finite rank n",
    "H_2: Identify Aut(F_n / F_n') with the general linear group GL_n(Z)",
    "¬Q: The homomorphism phi is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2