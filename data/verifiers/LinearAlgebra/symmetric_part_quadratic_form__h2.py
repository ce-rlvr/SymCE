import sympy as sp
from sympy import Matrix, eye, zeros
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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness is expected to provide both matrices A and S, 
    either as a tuple (A, S) or a dictionary {'A': A, 'S': S}.
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            S = witness.get('S')
        else:
            A, S = witness
            
        if not isinstance(A, Matrix):
            A = Matrix(A)
        if not isinstance(S, Matrix):
            S = Matrix(S)
    except Exception:
        return [False, False]

    # H_1: A is an n x n matrix with real entries
    # (We also verify S is a real matrix of the same dimensions to ensure the conclusion is well-formed)
    try:
        h1 = A.is_square and S.is_square and A.shape == S.shape
        if h1:
            for e in A:
                if not e.is_real:
                    h1 = False
                    break
            if h1:
                for e in S:
                    if not e.is_real:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # ¬Q: The conclusion FAILS at the witness.
    # The conclusion is: For all x in R^n, x^T A x = x^T S x.
    # This equality holds for all x if and only if the symmetric parts of A and S are equal.
    # Therefore, the conclusion fails (neg_Q is True) iff A + A^T != S + S^T.
    try:
        diff = sp.simplify((A + A.T) - (S + S.T))
        neg_q = diff != sp.zeros(*A.shape)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "¬Q: There exists x in R^n such that x^T A x != x^T S x"
]

N_HYP = 1
NEG_Q_INDEX = 1