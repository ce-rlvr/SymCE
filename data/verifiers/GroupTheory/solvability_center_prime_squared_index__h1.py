import sympy
import math
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
            try:
                h1 = sympy.isprime(p)
            except Exception:
                h1 = False
            try:
                Z = G.center()
                idx = G.order() // Z.order()
                h2 = (idx == p**2)
            except Exception:
                h2 = False
        else:
            G = witness
            try:
                Z = G.center()
                idx = G.order() // Z.order()
                root = math.isqrt(idx)
                if root**2 == idx and sympy.isprime(root):
                    h1 = True
                    h2 = True
            except Exception:
                pass
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness
        neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The index of the center Z(G) in G is exactly p^2",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2