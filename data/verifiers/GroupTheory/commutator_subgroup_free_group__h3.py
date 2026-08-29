import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    # H1: F is a free group of finite rank n
    h1 = False
    n = 0
    try:
        if type(witness).__name__ == 'FreeGroup':
            h1 = True
            n = len(witness.generators)
        elif type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0:
            h1 = True
            n = len(witness.generators)
        elif isinstance(witness, (int, sympy.Integer)) and witness >= 0:
            # Allow the witness to be just the rank n
            h1 = True
            n = int(witness)
    except Exception:
        pass

    # H2: n is greater than or equal to 2
    h2 = False
    try:
        if h1:
            h2 = bool(n >= 2)
    except Exception:
        pass

    # neg_Q: F' is NOT a free group of countably infinite rank.
    # By the Nielsen-Schreier theorem and Schreier index formula, the commutator 
    # subgroup of a free group of rank n is free of countably infinite rank iff n >= 2.
    neg_q = False
    try:
        if h1:
            is_countably_infinite = (n >= 2)
            neg_q = not is_countably_infinite
        else:
            # If it's not a free group, we cannot guarantee F' is free of countably infinite rank.
            neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank n",
    "H_2: n is greater than or equal to 2",
    "¬Q: F' is not a free group of countably infinite rank"
]

N_HYP = 2
NEG_Q_INDEX = 2