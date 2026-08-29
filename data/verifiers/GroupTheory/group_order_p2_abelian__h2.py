import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
    h1_ok = False
    neg_q_ok = False
    
    try:
        # The witness is expected to provide both the group G and the prime p.
        # It can be passed as a tuple: (G, p)
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = None
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        if p is not None:
            h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # ¬Q: The center Z(G) is not equal to G (i.e., G is not abelian)
    try:
        neg_q_ok = not bool(G.is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The center Z(G) is not equal to G (G is not abelian)"
]

N_HYP = 1
NEG_Q_INDEX = 1