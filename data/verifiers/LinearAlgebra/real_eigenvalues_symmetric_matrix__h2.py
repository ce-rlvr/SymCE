import sympy as sp
from sympy import Matrix, eye, zeros, I, pi, Rational, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import MatrixBase

# Standard algebra objects
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
    # Unpack witness: we expect a matrix A and a scalar lambda
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            lam = witness.get('lambda', witness.get('lam'))
        elif hasattr(witness, 'A') and (hasattr(witness, 'lam') or hasattr(witness, 'lambda_')):
            A = witness.A
            lam = getattr(witness, 'lam', getattr(witness, 'lambda_', None))
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, lam = witness
        else:
            A, lam = None, None
    except Exception:
        A, lam = None, None

    # H_1: Let A be an n \times n symmetric matrix with real entries.
    h1_ok = False
    try:
        if isinstance(A, MatrixBase) and A.is_square and A == A.T:
            h1_ok = True
            for val in A:
                if hasattr(val, 'is_real') and val.is_real is not None:
                    if not val.is_real:
                        h1_ok = False
                        break
                else:
                    try:
                        c = complex(val)
                        if c.imag != 0:
                            h1_ok = False
                            break
                    except Exception:
                        # If it cannot be evaluated to a complex number and lacks is_real=True,
                        # we cannot guarantee it is real.
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # ¬Q: The eigenvalue \lambda is NOT a real number.
    neg_q = False
    try:
        if lam is not None:
            if hasattr(lam, 'is_real') and lam.is_real is not None:
                neg_q = not lam.is_real
            else:
                try:
                    c = complex(lam)
                    neg_q = c.imag != 0
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n \\times n symmetric matrix with real entries",
    "¬Q: The eigenvalue \\lambda is not a real number"
]

N_HYP = 1
NEG_Q_INDEX = 1