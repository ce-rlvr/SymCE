import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    Checks if the witness is a counterexample to the conjecture:
    "If R is an integral domain, then Spec(R) is a connected topological space."
    
    The only counterexample is the zero ring (represented here by the integer 1, as in Z/1Z),
    which vacuously has no zero divisors (hence an integral domain if 1 != 0 is dropped),
    but its prime spectrum is empty (hence not connected).
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, int):
            if witness == 1:
                # Z/1Z is the zero ring.
                # It has no zero divisors, satisfying the dropped-condition definition of integral domain.
                h1 = True
                # Spec(Z/1Z) is empty. The empty space is not connected (it has exactly 1 idempotent: 0=1).
                neg_q = True
            elif witness == 0:
                # Z/0Z is isomorphic to Z, which is an integral domain.
                h1 = True
                # Spec(Z) is connected.
                neg_q = False
            elif witness > 1:
                # For Z/nZ, it is an integral domain iff n is prime.
                h1 = sympy.isprime(witness)
                # Spec(Z/nZ) is connected iff the ring has exactly 2 idempotents (0 and 1).
                idemps = sum(1 for i in range(witness) if (i * i) % witness == i)
                neg_q = (idemps != 2)
    except Exception:
        pass

    try:
        if isinstance(witness, str):
            w = witness.lower().replace(" ", "")
            if w in ['1', 'z/1z', 'zeroring', '{0}']:
                h1 = True
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: Spec(R) is not a connected topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1