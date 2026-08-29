import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness) -> list[bool]:
    """
    Given a witness (which represents the parameter p for the group Z(p^\infty)),
    check if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: G is the Prüfer p-group Z(p^\infty)
    # This implies the witness p must be a valid base for the group (an integer >= 2).
    try:
        h1_ok = isinstance(witness, (int, sympy.Integer)) and witness >= 2
    except Exception:
        h1_ok = False

    # ¬Q: The endomorphism ring of G is NOT isomorphic to the ring of p-adic integers Z_p.
    # The theorem holds when p is prime. If p is composite, the conclusion fails 
    # because Z_p is not the integral domain of p-adic integers.
    try:
        neg_q_ok = not sympy.isprime(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is the Prüfer p-group Z(p^\infty) (witness is p >= 2)",
    "¬Q: The endomorphism ring is not the ring of p-adic integers (p is not prime)"
]

N_HYP = 1
NEG_Q_INDEX = 1