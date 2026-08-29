import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    Checks if the witness is a counterexample to the false conjecture.
    The dropped hypothesis from the true theorem is that n is a positive integer (n > 0).
    In formal systems like Lean, a "primitive 0-th root of unity" is defined as an element 
    of infinite order. For n = 0, the Galois group of Q(zeta_0)/Q (e.g., for zeta_0 = 2) 
    is trivial, but (Z/0Z)^x is isomorphic to Z^x = {1, -1}, which has order 2. 
    Thus, they are not isomorphic, making n = 0 the counterexample.
    """
    # Extract n from the witness
    if isinstance(witness, dict):
        if 'n' in witness:
            n = witness['n']
        else:
            n = witness
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 1:
            n = witness[0]
        else:
            return [False, False]
    else:
        n = witness

    try:
        # H_1: \zeta_n is a primitive n-th root of unity
        # We verify that n is a valid integer index for which such a root could exist.
        if isinstance(n, bool):
            h1_ok = False
        else:
            n_val = int(n)
            h1_ok = (n_val == n)
    except Exception:
        h1_ok = False

    try:
        # \neg Q: The Galois group Gal(Q(\zeta_n)/Q) is NOT isomorphic to (Z/nZ)^x
        # For all n > 0 (and n < 0), the groups are isomorphic.
        # For n = 0, they are not isomorphic.
        if h1_ok and int(n) == 0:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \u03b6_n is a primitive n-th root of unity",
    "\u00acQ: The Galois group Gal(\u211a(\u03b6_n)/\u211a) is not isomorphic to (\u2124/n\u2124)^\u00d7"
]

N_HYP = 1
NEG_Q_INDEX = 1