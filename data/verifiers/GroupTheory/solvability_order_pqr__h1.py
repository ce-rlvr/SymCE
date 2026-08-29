import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            G, p, q, r = witness
            h1 = sympy.isprime(p) and sympy.isprime(q) and sympy.isprime(r) and len({p, q, r}) == 3
            h2 = (G.order() == p * q * r)
        else:
            G = witness
            order = G.order()
            factors = sympy.ntheory.factorint(order)
            primes = list(factors.keys())
            if len(primes) >= 3:
                h1 = True
                h2 = (len(primes) == 3 and order == primes[0] * primes[1] * primes[2])
            else:
                h1 = False
                h2 = False
    except Exception:
        h1 = False
        h2 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            G = witness[0]
        else:
            G = witness
            
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p, q, and r are distinct prime numbers",
    "H_2: The order of G is pqr",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2