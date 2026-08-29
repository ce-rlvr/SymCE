import sympy
from sympy import MatrixBase, Abs, simplify, eye, zeros, Rational, Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            c = witness.get('c')
        elif isinstance(witness, tuple) and len(witness) == 2:
            A, c = witness
        else:
            A, c = None, None
    except Exception:
        A, c = None, None

    # H_1: A is an m x n matrix over the complex numbers.
    try:
        h1 = isinstance(A, MatrixBase)
    except Exception:
        h1 = False

    # neg_Q: The conclusion FAILS at the witness.
    try:
        if A is None or c is None:
            neg_q = False
        else:
            cA = c * A
            sv_cA = cA.singular_values()
            sv_A = A.singular_values()
            
            try:
                if isinstance(c, MatrixBase) and c.is_square:
                    abs_c = c.det()
                else:
                    abs_c = Abs(c)
            except Exception:
                abs_c = Abs(c)
                
            if len(sv_cA) < len(sv_A):
                conclusion_holds = False
            else:
                conclusion_holds = True
                for val_cA, val_A in zip(sv_cA, sv_A):
                    diff = simplify(val_cA - abs_c * val_A)
                    if diff != 0:
                        try:
                            if abs(complex(diff.evalf())) > 1e-9:
                                conclusion_holds = False
                                break
                        except Exception:
                            conclusion_holds = False
                            break
            neg_q = not conclusion_holds
    except Exception:
        # If evaluating the conclusion raises an exception (e.g., dimension mismatch),
        # the conclusion is considered to fail.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over the complex numbers",
    "¬Q: The singular values of cA are not equal to |c| times the singular values of A"
]

N_HYP = 1
NEG_Q_INDEX = 1