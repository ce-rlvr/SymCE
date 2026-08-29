import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a candidate prime number p.
    """
    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(witness))
    except Exception:
        h1_ok = False

    # H_2: \mathbb{Q}_p is the field of p-adic numbers equipped with the standard p-adic absolute value
    # This is a definitional hypothesis establishing the context for p.
    h2_ok = True

    # ¬Q: \overline{\mathbb{Q}_p} is complete with respect to the extended p-adic absolute value
    # Fact: For any prime p, the algebraic closure of the p-adic numbers is NEVER complete.
    # Its completion is \mathbb{C}_p. Thus, the conclusion "\overline{\mathbb{Q}_p} is not complete" 
    # is always TRUE for any valid prime p, meaning its negation is always FALSE.
    try:
        neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: \mathbb{Q}_p is the field of p-adic numbers equipped with the standard p-adic absolute value",
    "¬Q: \overline{\mathbb{Q}_p} is complete with respect to the extended p-adic absolute value"
]

N_HYP = 2
NEG_Q_INDEX = 2