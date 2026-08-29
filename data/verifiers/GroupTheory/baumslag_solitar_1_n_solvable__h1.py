import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be an integer n, representing the parameter for BS(1, n).
    Alternatively, it could be a tuple (m, n) where m == 1.
    """
    h1 = False
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            m, n = witness
            if isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)):
                if int(m) == 1:
                    h1 = True
    except Exception:
        pass

    # The Baumslag-Solitar group BS(1, n) is isomorphic to the semidirect product
    # of Z[1/n] and Z. Its commutator subgroup is abelian, meaning BS(1, n) is
    # always metabelian, and therefore always solvable.
    # Since the conclusion "G is solvable" is ALWAYS TRUE for BS(1, n),
    # its negation is ALWAYS FALSE.
    neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the Baumslag-Solitar group BS(1, n)",
    "¬Q: The group G is not solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1