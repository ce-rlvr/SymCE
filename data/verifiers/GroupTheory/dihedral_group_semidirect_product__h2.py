import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    Checks whether the given witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        # Extract n from the witness
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('N', None))
        elif isinstance(witness, (tuple, list)):
            n = witness[0]
        else:
            n = witness
            
        if isinstance(n, (int, sympy.Integer)):
            h1 = bool(n >= 3)
        elif isinstance(n, float) and n.is_integer():
            h1 = bool(n >= 3)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # H2 is a descriptive hypothesis defining the homomorphism phi.
        # It is vacuously satisfied as a definition once a valid n is provided.
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            # The conclusion states D_{2n} is isomorphic to Z_n ⋊_phi Z_2.
            # The order of the dihedral group D_{2n} (degree 2n) is 4n.
            # The order of the external semidirect product Z_n ⋊_phi Z_2 is 2n.
            # Since 4n != 2n for any n >= 3, the two groups are never isomorphic.
            # Therefore, the conclusion always fails at the witness, making its negation True.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: phi is the homomorphism mapping the non-identity element of Z_2 to the inversion automorphism of Z_n",
    "¬Q: D_{2n} is not isomorphic to the external semidirect product Z_n ⋊_phi Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2