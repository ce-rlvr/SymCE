import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import totient

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = G.order() if hasattr(G, 'order') else None
    except Exception:
        G = witness
        n = None

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1 and n is not None:
            h2 = (G.order() == n)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and h2:
            order_G = G.order()
            if order_G <= 5000:
                generators_count = sum(1 for g in G.elements if g.order() == order_G)
                expected = totient(order_G)
                neg_q = (generators_count != expected)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is a finite group",
    "H_2: the order of G is n",
    "¬Q: The number of elements g in G such that <g> = G is not phi(n)"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2