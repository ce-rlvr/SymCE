import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix, eye, zeros

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
    neg_q = False
    
    try:
        # If the witness is a matrix (representing a subspace, linear map, or bilinear form),
        # the annihilator is non-trivial if and only if the matrix does not have full rank
        # in at least one of its dimensions (i.e., it has a non-trivial left or right null space).
        if hasattr(witness, 'rank') and hasattr(witness, 'rows') and hasattr(witness, 'cols'):
            r = witness.rank()
            if r < witness.rows or r < witness.cols:
                neg_q = True
        elif isinstance(witness, (list, tuple)):
            M = Matrix(witness)
            r = M.rank()
            if r < M.rows or r < M.cols:
                neg_q = True
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The annihilator V^0 is not the trivial subspace {0} (witness does not have full rank)"
]

N_HYP = 0
NEG_Q_INDEX = 0