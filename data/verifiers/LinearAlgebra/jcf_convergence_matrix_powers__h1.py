import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "¬Q: The equivalence (A^m -> 0 iff all |lambda| < 1) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness) -> list[bool]:
    try:
        # Convert standard Python lists/tuples to sympy Matrix
        if isinstance(witness, (list, tuple)):
            witness = sp.Matrix(witness)
            
        # The witness must be a matrix
        if not isinstance(witness, sp.MatrixBase):
            return [False]
            
        if witness.is_square:
            # The theorem (A^m -> 0 iff all |\lambda| < 1) is universally true 
            # for all square matrices over the complex numbers. 
            # Therefore, no square matrix can be a valid counterexample.
            return [False]
        else:
            # The dropped hypothesis is that A must be a square matrix.
            # For a non-square matrix:
            # 1. A^m is undefined, so the sequence does not converge to the zero matrix (LHS is False).
            # 2. A has no eigenvalues, so the statement "every eigenvalue satisfies |\lambda| < 1" 
            #    is vacuously true (RHS is True).
            # The equivalence (False <-> True) is False, meaning the conclusion fails.
            return [True]
            
    except Exception:
        return [False]