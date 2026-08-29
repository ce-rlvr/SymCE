import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            e = witness.get('e')
        else:
            G, p, e = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: p divides the order of G
    try:
        if hasattr(G, 'order'):
            if callable(G.order):
                order = G.order()
            else:
                order = G.order
        else:
            if hasattr(G, 'elements'):
                order = len(list(G.elements))
            elif hasattr(G, 'generate'):
                order = len(list(G.generate()))
            else:
                order = len(list(G))
        h2 = bool(order % p == 0)
    except Exception:
        h2 = False

    # H_3: e is the identity element of G
    try:
        if hasattr(G, 'identity'):
            h3 = bool(e == G.identity)
        else:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif hasattr(G, 'generate'):
                elements = list(G.generate())
            else:
                elements = list(G)
            
            h3 = (e in elements)
            if h3:
                for x in elements:
                    if x * e != x or e * x != x:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: The number of elements x in G such that x^p = e is NOT a multiple of p
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        count = 0
        for x in elements:
            try:
                val = x**p
            except Exception:
                val = x
                for _ in range(p - 1):
                    val = val * x
            if val == e:
                count += 1
        neg_q = bool(count % p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides the order of G",
    "H_3: e is the identity element of G",
    "¬Q: The number of elements x in G such that x^p = e is not a multiple of p"
]

N_HYP = 3
NEG_Q_INDEX = 3