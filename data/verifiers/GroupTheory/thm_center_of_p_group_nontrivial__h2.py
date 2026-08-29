import sympy
from sympy.ntheory import isprime
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The order of G is p^n for some integer n >= 1",
    "¬Q: The center of G, Z(G), contains at most one element"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # The witness is expected to be a tuple (G, p) or (p, G)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[0], 'order') or hasattr(witness[0], 'center'):
                G, p = witness
            else:
                p, G = witness
        else:
            if hasattr(witness, 'p'):
                G = witness
                p = witness.p
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: The order of G is p^n for some integer n >= 1
    try:
        if callable(getattr(G, 'order', None)):
            order = G.order()
        else:
            order = G.order
            
        if int(order) != order:
            h2 = False
        else:
            p_val = int(p)
            if p_val > 1:
                temp = int(order)
                n = 0
                while temp % p_val == 0:
                    temp //= p_val
                    n += 1
                h2 = bool(temp == 1 and n >= 1)
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: The center of G, Z(G), contains strictly more than one element
    # Negation: Z(G) contains at most one element
    try:
        if callable(getattr(G, 'center', None)):
            center = G.center()
        else:
            center = G.center
            
        if callable(getattr(center, 'order', None)):
            c_order = center.order()
        elif hasattr(center, 'order'):
            c_order = center.order
        else:
            c_order = len(list(center))
            
        neg_q = bool(c_order <= 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]