import sympy
from sympy import eye, zeros, Rational, Integer
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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

class AbstractRing:
    """
    A helper class to represent abstract rings with specific properties,
    since SymPy cannot natively represent arbitrary non-Noetherian local rings.
    """
    def __init__(self, is_commutative=True, has_identity=True, is_local=False, intersection_m_n_is_zero=True):
        self.is_commutative = is_commutative
        self.has_identity = has_identity
        self.is_local = is_local
        self.intersection_m_n_is_zero = intersection_m_n_is_zero

# A standard counterexample to the Krull Intersection Theorem without the Noetherian hypothesis:
# The ring of germs of smooth real-valued functions at the origin.
# Its unique maximal ideal consists of germs vanishing at 0.
# The intersection of powers of this maximal ideal contains flat functions (e.g., e^{-1/x^2}),
# which are non-zero, so the intersection is not {0}.
GermsOfSmoothFunctions = AbstractRing(
    is_commutative=True,
    has_identity=True,
    is_local=True,
    intersection_m_n_is_zero=False
)

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring with identity
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_commutative", False) and witness.get("has_identity", False))
        else:
            h1 = bool(witness.is_commutative and witness.has_identity)
    except Exception:
        h1 = False

    # H_2: R is a local ring with unique maximal ideal m
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("is_local", False))
        else:
            h2 = bool(witness.is_local)
    except Exception:
        h2 = False

    # ¬Q: The intersection \bigcap_{n=1}^{\infty} m^n is not equal to {0}
    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get("intersection_m_n_is_zero", True))
        else:
            neg_q = not bool(witness.intersection_m_n_is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a local ring with unique maximal ideal m",
    "¬Q: The intersection \\bigcap_{n=1}^{\\infty} m^n is not equal to {0}"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2