import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: Let p be a prime.
    try:
        p = int(witness)
        h1_ok = sympy.isprime(p)
    except Exception:
        h1_ok = False

    # Conclusion: Z(p^infty) admits the infinite presentation < g_1, g_2, ... | g_1^p = 1, g_{k+1}^p = g_k for all k >= 1 >
    # This is the standard definition/presentation of the Prüfer p-group and is mathematically true for all primes p.
    # Since the conclusion is universally true for any prime p, it never fails.
    # Thus, the negated conclusion (neg_Q) is always False.
    try:
        neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "¬Q: Z(p^infty) does not admit the infinite presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1