import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    try:
        rank = -1
        if (isinstance(witness, int) and not isinstance(witness, bool)) or \
           (hasattr(witness, 'is_integer') and witness.is_integer):
            if witness >= 0:
                rank = int(witness)
        elif type(witness).__name__ == 'FreeGroup':
            rank = len(witness.generators)
        elif type(witness).__name__ == 'FpGroup':
            if len(witness.relators) == 0:
                rank = len(witness.generators)
        elif hasattr(witness, 'is_trivial'):
            if witness.is_trivial:
                rank = 0
                
        h1 = (rank >= 0)
    except Exception:
        h1 = False

    try:
        if rank >= 0:
            # A free group of rank r is co-Hopfian (every injective endomorphism is surjective)
            # if and only if r = 0 (the trivial group).
            neg_q = (rank == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: Every injective group homomorphism from F to F is surjective"
]

N_HYP = 1
NEG_Q_INDEX = 1