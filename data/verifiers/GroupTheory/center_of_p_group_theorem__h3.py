import sympy
import sympy.ntheory
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # Unpack witness
    p = None
    G = None
    if isinstance(witness, dict):
        p = witness.get('p')
        G = witness.get('G')
    elif isinstance(witness, tuple) and len(witness) == 2:
        if hasattr(witness[0], 'order'):
            G = witness[0]
            p = witness[1]
        elif hasattr(witness[1], 'order'):
            G = witness[1]
            p = witness[0]
        else:
            p, G = witness
    else:
        G = witness
        try:
            order = G.order()
            factors = sympy.ntheory.factorint(order)
            if len(factors) == 1:
                p = list(factors.keys())[0]
        except Exception:
            pass

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: G is a finite p-group such that |G| = p^n for some integer n >= 1
    try:
        order = G.order()
        if order < 2 or not isinstance(p, (int, sympy.Integer)) or p < 2:
            h2 = False
        else:
            temp = order
            n = 0
            while temp % p == 0:
                temp //= p
                n += 1
            h2 = bool(temp == 1 and n >= 1)
    except Exception:
        h2 = False

    # ¬Q: The set of fixed points of the action, which is the center Z(G), has size <= 1
    try:
        center = G.center()
        neg_q = bool(center.order() <= 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group such that |G| = p^n for some integer n >= 1",
    "¬Q: The center Z(G) has size <= 1"
]

N_HYP = 2
NEG_Q_INDEX = 2