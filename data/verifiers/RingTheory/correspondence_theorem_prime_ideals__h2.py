import sympy
from sympy import *
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)

def check_attr(witness, attr_name, default=False):
    """Helper to extract boolean properties from a witness (dict or object)."""
    if isinstance(witness, dict) and attr_name in witness:
        val = witness[attr_name]
        return val() if callable(val) else val
    if hasattr(witness, attr_name):
        val = getattr(witness, attr_name)
        return val() if callable(val) else val
    return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a dictionary or object providing the following boolean flags/methods:
      - is_commutative_ring_with_identity
      - is_canonical_projection_homomorphism
      - is_prime_ideal_bijection
    """
    # H1: R is a commutative ring with identity
    try:
        h1_ok = bool(check_attr(witness, 'is_commutative_ring_with_identity', False))
    except Exception:
        h1_ok = False

    # H2: \pi: R \to R/I is the canonical projection homomorphism
    try:
        h2_ok = bool(check_attr(witness, 'is_canonical_projection_homomorphism', False))
    except Exception:
        h2_ok = False

    # neg_Q: The mapping P \mapsto \pi(P) is NOT a bijection between the set of prime ideals 
    # of R containing I and the set of prime ideals of the quotient ring R/I.
    try:
        bijection = check_attr(witness, 'is_prime_ideal_bijection', True)
        neg_q_ok = not bool(bijection)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: \\pi: R \\to R/I is the canonical projection homomorphism",
    "¬Q: The mapping P \\mapsto \\pi(P) is not a bijection between the set of prime ideals of R containing I and the set of prime ideals of the quotient ring R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2