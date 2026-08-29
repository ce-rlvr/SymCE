import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint

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

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: The order of G is exactly p^2 * q^2",
    "¬Q: G is a simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    G = None
    p = None
    q = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            if hasattr(G, 'order'):
                if callable(G.order):
                    order = G.order()
                else:
                    order = G.order
                factors = factorint(order)
                if len(factors) == 2:
                    primes = list(factors.keys())
                    if factors[primes[0]] == 2 and factors[primes[1]] == 2:
                        p, q = primes[0], primes[1]
    except Exception:
        pass

    try:
        h1 = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h1 = False

    try:
        if callable(G.order):
            order = G.order()
        else:
            order = G.order
        h2 = bool(order == p**2 * q**2)
    except Exception:
        h2 = False

    try:
        if hasattr(G, 'is_simple'):
            if callable(G.is_simple):
                neg_q = bool(G.is_simple())
            else:
                neg_q = bool(G.is_simple)
        elif hasattr(G, 'composition_series'):
            if callable(G.composition_series):
                neg_q = bool(len(G.composition_series()) == 2)
            else:
                neg_q = bool(len(G.composition_series) == 2)
        elif hasattr(G, 'normal_subgroups'):
            if callable(G.normal_subgroups):
                neg_q = bool(len(G.normal_subgroups()) == 2)
            else:
                neg_q = bool(len(G.normal_subgroups) == 2)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]