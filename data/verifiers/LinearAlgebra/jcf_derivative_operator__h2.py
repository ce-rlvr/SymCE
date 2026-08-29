import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    Checks whether the given witness (n) satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    # Check Hypothesis 1: n must be an integer for the space of polynomials 
    # of degree at most n to be well-defined in this context.
    try:
        if isinstance(witness, int):
            h1 = True
            n_val = witness
        elif isinstance(witness, float):
            h1 = witness.is_integer()
            n_val = int(witness)
        else:
            n = sp.sympify(witness)
            h1 = bool(n.is_integer)
            n_val = int(n)
    except Exception:
        h1 = False
        n_val = 0

    # Check Negated Conclusion:
    # The conclusion states that the Jordan canonical form of D consists of a 
    # SINGLE nilpotent Jordan block of size n+1.
    # For n >= 0, the dimension of V is n+1, and D is a single nilpotent block of size n+1.
    # For n < 0 (e.g., n = -1), the dimension of V is 0. The matrix of D is 0x0.
    # A 0x0 matrix has 0 Jordan blocks, which is not a "single" block.
    # Furthermore, if n < -1, a block of negative size is impossible.
    # Thus, the conclusion fails (neg_q is True) if and only if n < 0.
    try:
        if not h1:
            neg_q = False
        else:
            if n_val < 0:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is the vector space of polynomials with complex coefficients of degree at most n",
    "¬Q: The Jordan canonical form of the operator D does not consist of a single nilpotent Jordan block of size n+1"
]

N_HYP = 1
NEG_Q_INDEX = 1