import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# --- Top-level setup ---

class CommutativeRing:
    def __init__(self, name, has_identity=True):
        self.name = name
        self.has_identity = has_identity
    def __str__(self):
        return self.name

class RModule:
    def __init__(self, name, ring):
        self.name = name
        self.ring = ring
    def __str__(self):
        return self.name

class MultiplicativelyClosedSubset:
    def __init__(self, name, ring):
        self.name = name
        self.ring = ring
    def __str__(self):
        return self.name

# Standard group and matrix objects
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

# Ring theory specific objects for the witness
Z_ring = CommutativeRing("Z")
Q_ring = CommutativeRing("Q")

N_Z = RModule("N_Z", Z_ring)
N_Q = RModule("N_Q", Q_ring)

S_Z = MultiplicativelyClosedSubset("S_Z", Z_ring)
S_Q = MultiplicativelyClosedSubset("S_Q", Q_ring)

M_Z = RModule("M_Z", Z_ring)
M_Q = RModule("M_Q", Q_ring)
M_not_module = "Not a module"

# --- Verifier ---

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide R, M, N, and S.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            M = witness.get("M")
            N = witness.get("N")
            S = witness.get("S")
        else:
            R, M, N, S = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = isinstance(R, CommutativeRing) and R.has_identity
    except Exception:
        h1 = False

    # H_2: N is an R-module
    try:
        h2 = isinstance(N, RModule) and N.ring == R
    except Exception:
        h2 = False

    # H_3: S is a multiplicatively closed subset of R
    try:
        h3 = isinstance(S, MultiplicativelyClosedSubset) and S.ring == R
    except Exception:
        h3 = False

    # ¬Q: S^{-1}(M \otimes_R N) is NOT isomorphic to S^{-1}M \otimes_{S^{-1}R} S^{-1}N
    try:
        # The isomorphism requires M to be an R-module.
        # If M is not an R-module, the tensor product M \otimes_R N is undefined,
        # hence the isomorphism does not exist and the conclusion fails.
        is_R_module = isinstance(M, RModule) and M.ring == R
        neg_q = not is_R_module
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: N is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}(M \\otimes_R N) is not isomorphic to S^{-1}M \\otimes_{S^{-1}R} S^{-1}N"
]

N_HYP = 3
NEG_Q_INDEX = 3