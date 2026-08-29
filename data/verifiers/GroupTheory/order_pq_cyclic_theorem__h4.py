import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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
    # H_1: G is a finite group
    try:
        h1 = hasattr(witness, 'order') and hasattr(witness, 'is_cyclic')
        if h1:
            order = witness.order()
            if order == sympy.oo or order == float('inf'):
                h1 = False
            elif order < 1:
                h1 = False
    except Exception:
        h1 = False

    # H_2: The order of G is pq, where p and q are prime numbers
    try:
        if h1:
            order = witness.order()
            factors = factorint(order)
            # sum of exponents is exactly 2 means it's a product of two primes
            h2 = sum(factors.values()) == 2
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: p < q
    try:
        if h1 and h2:
            order = witness.order()
            factors = factorint(order)
            # Since sum of exponents is 2, having 2 distinct prime factors means p != q.
            # Thus one must be strictly less than the other (p < q).
            h3 = len(factors) == 2
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: G is NOT cyclic
    try:
        if h1:
            is_cyc = witness.is_cyclic
            if callable(is_cyc):
                is_cyc = is_cyc()
            neg_q = not is_cyc
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is pq, where p and q are prime numbers",
    "H_3: p < q",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3