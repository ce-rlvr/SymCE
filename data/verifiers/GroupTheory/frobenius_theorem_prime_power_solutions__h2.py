import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, p), checks the remaining hypotheses and the negated conclusion.
    Returns [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok].
    """
    try:
        G, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        # Check if G has an order property and it's finite
        order = G.order()
        h1_ok = order > 0 and order < float('inf')
    except Exception:
        h1_ok = False

    # H_2: p divides the order of G
    try:
        h2_ok = (G.order() % p == 0)
    except Exception:
        h2_ok = False

    # H_3: e is the identity element of G
    try:
        # This hypothesis just states the existence of an identity element,
        # which is true for any valid group object in SymPy.
        e = G.identity
        h3_ok = e in G
    except Exception:
        h3_ok = False

    # ¬Q: The number of elements x \in G such that x^p = e is NOT a multiple of p
    try:
        e = G.identity
        count = 0
        for x in G.elements:
            if x**p == e:
                count += 1
        neg_q_ok = (count % p != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p divides the order of G",
    "H_3: e is the identity element of G",
    "¬Q: The number of elements x \\in G such that x^p = e is not a multiple of p"
]

N_HYP = 3
NEG_Q_INDEX = 3