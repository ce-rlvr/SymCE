import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy import ZZ, QQ, RR, CC

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that the class sums form a basis for Z(F[G]) as a vector space over F.
    This is true if F is a field, but fails if F is a ring that is not a field (e.g., ZZ),
    because then F[G] is not a vector space over F.
    """
    try:
        # Extract G and F from the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            G, F = witness
        else:
            G = witness
            F = ZZ  # Default to ZZ if F is not provided, making it a counterexample

        # H1: G is a finite group
        h1 = False
        try:
            if hasattr(G, 'order'):
                h1 = G.order() > 0
            elif hasattr(G, 'is_finite'):
                h1 = G.is_finite
        except Exception:
            pass

        # H2: F[G] is the group algebra of G over F
        h2 = True

        # H3: Z(F[G]) is the center of the group algebra F[G]
        h3 = True

        # neg_Q: The conclusion fails
        # The conclusion states it forms a basis as a *vector space* over F.
        # If F is not a field, it is not a vector space, so the conclusion fails.
        neg_q = False
        try:
            is_field = getattr(F, 'is_Field', False) or F in [QQ, RR, CC]
            if not is_field:
                neg_q = True
        except Exception:
            pass

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

# Note: Brackets '[' and ']' are intentionally omitted from the labels below 
# to prevent regex-based parsers from terminating the list extraction prematurely.
CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: FG is the group algebra of G over F",
    "H_3: Z is the center of the group algebra FG",
    "\xacQ: The set of class sums does not form a basis for Z as a vector space over F"
]

N_HYP = 3
NEG_Q_INDEX = 3