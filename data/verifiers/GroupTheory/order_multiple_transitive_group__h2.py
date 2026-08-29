import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        G, n, k = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = isinstance(n, int) and isinstance(k, int) and 1 <= k <= n and hasattr(G, 'order')
    except Exception:
        h1_ok = False

    try:
        order_G = int(G.order())
        div = math.factorial(n) // math.factorial(n - k)
        neg_q_ok = (order_G % div != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n and k are integers with 1 <= k <= n",
    "¬Q: The order of G is not divisible by n! / (n-k)!"
]

N_HYP = 1
NEG_Q_INDEX = 1