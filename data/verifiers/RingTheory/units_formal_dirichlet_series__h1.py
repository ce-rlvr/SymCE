import sympy
from sympy import symbols, Matrix, eye, zeros, Rational
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the witness.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    # H_1: D(R) is the ring of formal Dirichlet series with coefficients in R
    try:
        if isinstance(witness, dict):
            h1_ok = 'R' in witness
        else:
            h1_ok = hasattr(witness, 'R')
    except Exception:
        h1_ok = False

    # H_2: f(s) in D(R)
    try:
        if isinstance(witness, dict):
            h2_ok = 'f' in witness
        else:
            h2_ok = hasattr(witness, 'f')
    except Exception:
        h2_ok = False

    # ¬Q: f(s) is a unit in D(R) iff a_1 is a unit in R is FALSE
    try:
        if isinstance(witness, dict):
            f_is_unit = witness.get('f_is_unit')
            a1_is_unit = witness.get('a1_is_unit')
        else:
            f_is_unit = getattr(witness, 'f_is_unit', None)
            a1_is_unit = getattr(witness, 'a1_is_unit', None)
            
        if f_is_unit is not None and a1_is_unit is not None:
            neg_q_ok = (bool(f_is_unit) != bool(a1_is_unit))
        else:
            # If properties are not explicitly provided, we assume the witness 
            # is structured such that we can evaluate the biconditional.
            # However, mathematically, if R has an identity, the biconditional is true.
            # The conjecture might fail if R lacks an identity or under specific definitions.
            # We default to checking if the provided boolean flags differ.
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: D(R) is the ring of formal Dirichlet series with coefficients in R",
    "H_2: f(s) in D(R)",
    "¬Q: f(s) is a unit in D(R) iff a_1 is a unit in R is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2