import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_order(g):
    if hasattr(g, 'order'):
        return int(g.order())
    if hasattr(g, 'is_Matrix') and g.is_Matrix:
        if not g.is_square:
            raise ValueError("Not a square matrix")
        I = eye(g.rows)
        if g == I:
            return 1
        curr = g
        for i in range(2, 1000):
            curr = curr * g
            if curr == I:
                return i
    raise ValueError("Could not determine order")

def conditions(witness) -> list[bool]:
    m = None
    n = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, g, h = witness
            try:
                h1 = bool(G.contains(g)) if hasattr(G, 'contains') else bool(g in G)
            except Exception:
                h1 = hasattr(g, '__mul__')
            try:
                h2 = bool(G.contains(h)) if hasattr(G, 'contains') else bool(h in G)
            except Exception:
                h2 = hasattr(h, '__mul__')
        elif isinstance(witness, tuple) and len(witness) == 2:
            g, h = witness
            h1 = hasattr(g, '__mul__')
            h2 = hasattr(h, '__mul__')
        else:
            return [False] * 7
    except Exception:
        return [False] * 7

    try:
        h3 = bool(g * h == h * g)
    except Exception:
        h3 = False

    try:
        m = get_order(g)
        h4 = m > 0
    except Exception:
        h4 = False

    try:
        n = get_order(h)
        h5 = n > 0
    except Exception:
        h5 = False

    try:
        if m is not None and n is not None:
            h6 = math.gcd(m, n) == 1
        else:
            h6 = False
    except Exception:
        h6 = False

    try:
        if m is not None and n is not None:
            gh = g * h
            gh_order = get_order(gh)
            neg_q = gh_order != m * n
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "H_2: h is an element of G",
    "H_3: g and h commute",
    "H_4: the order of g is a finite integer m",
    "H_5: the order of h is a finite integer n",
    "H_6: gcd(m, n) = 1",
    "¬Q: the order of the product gh is not exactly m * n"
]

N_HYP = 6
NEG_Q_INDEX = 6