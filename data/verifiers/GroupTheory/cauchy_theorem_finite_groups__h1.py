import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import isprime
import itertools

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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
        else:
            G, p = witness
    except Exception:
        return [False, False, False]

    order_G = None

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: p divides the order of G
    try:
        if hasattr(G, 'order') and callable(G.order):
            order_G = G.order()
        elif hasattr(G, 'order'):
            order_G = G.order
        else:
            order_G = len(G)
        
        if order_G is None:
            h2 = False
        else:
            h2 = bool(order_G % p == 0)
    except Exception:
        h2 = False

    # ¬Q: There is no element in G of order p
    try:
        from sympy import oo
        
        is_infinite = (order_G == oo) or (order_G is None)

        if hasattr(G, 'generate') and callable(G.generate):
            iterator = G.generate()
        elif hasattr(G, 'elements'):
            iterator = G.elements
        else:
            iterator = G
            
        if is_infinite:
            elements = itertools.islice(iterator, 2000)
        else:
            elements = iterator
            
        neg_q = True
        for x in elements:
            ox = None
            try:
                if hasattr(x, 'order') and callable(x.order):
                    ox = x.order()
                elif hasattr(x, 'order'):
                    ox = x.order
            except Exception:
                pass
            
            if ox == p:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides the order of G",
    "¬Q: There is no element in G of order p"
]

N_HYP = 2
NEG_Q_INDEX = 2