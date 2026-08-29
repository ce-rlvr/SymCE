import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, isprime
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: G is a finite group of order p^a q^b",
    "H_2: p and q are distinct primes",
    "H_3: p^a < q",
    "¬Q: The Sylow q-subgroup of G is not normal in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    G, p, q, a, b = None, None, None, None, None
    
    # Attempt to unpack the witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 5:
                G, p, q, a, b = witness
            elif len(witness) == 3:
                G, p, q = witness
                if hasattr(G, 'order'):
                    order = G.order()
                    temp = order
                    a = 0
                    while temp > 0 and temp % p == 0:
                        a += 1
                        temp //= p
                    b = 0
                    while temp > 0 and temp % q == 0:
                        b += 1
                        temp //= q
            else:
                G = witness[0]
        else:
            G = witness
            
        # If parameters are missing, try to deduce them from the group order
        if p is None or q is None:
            if hasattr(G, 'order'):
                order = G.order()
                factors = factorint(order)
                if len(factors) == 2:
                    p1, p2 = list(factors.keys())
                    a1, a2 = factors[p1], factors[p2]
                    if p1**a1 < p2:
                        p, q, a, b = p1, p2, a1, a2
                    else:
                        p, q, a, b = p2, p1, a2, a1
                elif len(factors) == 1:
                    p = list(factors.keys())[0]
                    q = 2 if p != 2 else 3
                    a = factors[p]
                    b = 0
                else:
                    p, q, a, b = 2, 3, 1, 1
    except Exception:
        pass

    # H_1: G is a finite group of order p^a q^b
    try:
        h1 = False
        if hasattr(G, 'order') and p is not None and q is not None and a is not None and b is not None:
            val = (p**a) * (q**b)
            if type(a) is int and type(b) is int:
                h1 = (G.order() == val)
            else:
                h1 = bool(abs(G.order() - float(val)) < 1e-7)
    except Exception:
        h1 = False

    # H_2: p and q are distinct primes
    try:
        h2 = bool(isprime(p) and isprime(q) and (p != q))
    except Exception:
        h2 = False

    # H_3: p^a < q
    try:
        h3 = bool((p**a) < q)
    except Exception:
        h3 = False

    # ¬Q: The Sylow q-subgroup of G is not normal in G
    try:
        neg_q_ok = False
        if hasattr(G, 'sylow_subgroup') and isprime(q):
            H = G.sylow_subgroup(q)
            is_normal = True
            for g in G.generators:
                for h in H.generators:
                    conj = g * h * (~g)
                    if not H.contains(conj):
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q_ok = not is_normal
    except Exception:
        neg_q_ok = False

    return [h1, h2, h3, neg_q_ok]