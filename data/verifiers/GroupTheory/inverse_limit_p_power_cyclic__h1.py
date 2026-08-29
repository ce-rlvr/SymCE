import sympy
import sympy.combinatorics
import sympy.matrices
from sympy import isprime

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract p from the witness
    try:
        if isinstance(witness, (tuple, list)):
            p = int(witness[0])
        else:
            p = int(witness)
        # p must be a positive integer to form the inverse system Z/p^nZ
        h1 = (p > 0)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (tuple, list)):
            p = int(witness[0])
        else:
            p = int(witness)
        # The natural projections are well-defined for any positive integer p
        h2 = (p > 0)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, (tuple, list)):
            p = int(witness[0])
        else:
            p = int(witness)
        # The conclusion fails if p is not a prime, because the p-adic integers
        # Z_p are defined (and form an integral domain/field of fractions) specifically for primes.
        # For composite p, the inverse limit is not the standard p-adic integers Z_p.
        neg_q = not isprime(p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: {G_n} is an inverse system of groups where G_n = Z/p^nZ",
    "H_2: The transition maps of the inverse system are the natural projections",
    "¬Q: The inverse limit is not isomorphic to the additive group of p-adic integers Z_p"
]

N_HYP = 2
NEG_Q_INDEX = 2