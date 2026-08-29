import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def conditions(witness) -> list[bool]:
    # The witness is expected to contain the group G, the element a, and the integer k.
    # It may optionally include n explicitly.
    try:
        if len(witness) == 3:
            G, a, k = witness
        elif len(witness) == 4:
            G, n_wit, a, k = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite cyclic group of order n, and a is an element of G
    try:
        h1_ok = False
        if hasattr(G, 'order') and hasattr(G, 'elements'):
            n = G.order()
            if n <= 1000:  # Prevent performance issues with excessively large groups
                is_cyclic = False
                for g in G.elements:
                    if g.order() == n:
                        is_cyclic = True
                        break
                if is_cyclic:
                    if a in G.elements:
                        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: k is an integer
    try:
        h2_ok = isinstance(k, int)
    except Exception:
        h2_ok = False

    # ¬Q: The order of the element a^k is NOT n / gcd(n, k)
    try:
        n = G.order()
        ak = a**k
        order_ak = ak.order()
        expected_order = n // math.gcd(n, k)
        neg_q_ok = order_ak != expected_order
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n, and a is an element of G",
    "H_2: k is an integer",
    "¬Q: The order of a^k is not n / gcd(n, k)"
]

N_HYP = 2
NEG_Q_INDEX = 2