import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)  # V4 is isomorphic to a subgroup of A4, but we'll just provide A4
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, p, k), checks if it is a counterexample to the false conjecture.
    The conjecture states: If p is prime, G has a conjugacy class of size p^k, and k > 0,
    then G is not a simple group.
    """
    try:
        G, p, k = witness
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H2: G contains a conjugacy class of size p^k
    try:
        target_size = p**k
        h2_ok = False
        if hasattr(G, 'conjugacy_classes'):
            classes = G.conjugacy_classes()
            for cls in classes:
                if len(cls) == target_size:
                    h2_ok = True
                    break
    except Exception:
        h2_ok = False

    # H3: k > 0
    try:
        h3_ok = bool(k > 0)
    except Exception:
        h3_ok = False

    # neg_Q: G IS a simple group (negation of "G is not a simple group")
    try:
        neg_q_ok = bool(G.is_simple)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G contains a conjugacy class of size p^k",
    "H_3: k > 0",
    "¬Q: G is a simple group"
]

N_HYP = 3
NEG_Q_INDEX = 3