import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    G = None
    p = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        elif isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
        else:
            G = witness
            
        if p is None and G is not None:
            try:
                if callable(G.order):
                    order = G.order()
                else:
                    order = G.order
                order_int = int(order)
                p_val = math.isqrt(order_int // 2)
                if 2 * p_val**2 == order_int:
                    p = p_val
            except Exception:
                pass
    except Exception:
        pass

    if p is None:
        p = 0

    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: The order of G is 2p^2
    try:
        if callable(G.order):
            order = G.order()
        else:
            order = G.order
        h2 = bool(int(order) == 2 * int(p)**2)
    except Exception:
        h2 = False

    # neg_Q: G is not a solvable group
    try:
        if callable(G.is_solvable):
            solvable = G.is_solvable()
        else:
            solvable = G.is_solvable
        neg_q = not bool(solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The order of G is 2p^2",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2