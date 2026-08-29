import math
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    G, e, m, n = None, None, None, None
    
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            e = witness.get('e')
            m = witness.get('m')
            n = witness.get('n')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, m = witness
            elif len(witness) == 3:
                G = witness[0]
                try:
                    if witness[1] == G.identity:
                        e = witness[1]
                        m = witness[2]
                    else:
                        m = witness[1]
                        n = witness[2]
                except Exception:
                    m = witness[1]
                    n = witness[2]
            elif len(witness) == 4:
                G, e, m, n = witness
                
        if e is None and hasattr(G, 'identity'):
            e = G.identity
        if n is None and hasattr(G, 'order'):
            n = G.order()
    except Exception:
        pass

    # H1: G is a cyclic group
    h1 = False
    try:
        if hasattr(G, 'is_cyclic'):
            h1 = bool(G.is_cyclic)
        elif hasattr(G, 'elements') and hasattr(G, 'order'):
            o = G.order()
            h1 = any(g.order() == o for g in G.elements)
    except Exception:
        h1 = False

    # H2: e is the identity element of G
    h2 = False
    try:
        if hasattr(G, 'identity'):
            h2 = (e == G.identity)
    except Exception:
        h2 = False

    # H3: m is an integer
    h3 = False
    try:
        h3 = isinstance(m, int) or (hasattr(m, 'is_integer') and m.is_integer)
        h3 = bool(h3)
    except Exception:
        h3 = False

    # neg_Q: The number of elements x in G satisfying x^m = e is exactly gcd(m,n)
    neg_q = False
    try:
        count = 0
        for x in G.elements:
            if (x**m) == e:
                count += 1
        try:
            if not (isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer)):
                neg_q = True
            else:
                expected = math.gcd(int(m), int(n))
                neg_q = (count != expected)
        except Exception:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: e is the identity element of G",
    "H_3: m is an integer",
    "¬Q: The number of elements x in G satisfying x^m = e is not exactly gcd(m,n)"
]

N_HYP = 3
NEG_Q_INDEX = 3