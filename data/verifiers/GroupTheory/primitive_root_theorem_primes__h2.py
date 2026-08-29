import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime, totient, n_order
import math

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
        p = int(witness)
        h1 = isprime(p)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p <= 1:
            is_cyclic_of_order_p_minus_1 = False
        else:
            tot = totient(p)
            if tot != p - 1:
                is_cyclic_of_order_p_minus_1 = False
            else:
                is_cyclic = False
                for g in range(1, p):
                    if math.gcd(g, p) == 1:
                        if n_order(g, p) == p - 1:
                            is_cyclic = True
                            break
                is_cyclic_of_order_p_minus_1 = is_cyclic
        neg_q = not is_cyclic_of_order_p_minus_1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: (Z/pZ)^x is not a cyclic group of order p-1"
]

N_HYP = 1
NEG_Q_INDEX = 1