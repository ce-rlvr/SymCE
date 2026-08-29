import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_conjugacy_class_sizes(G):
    try:
        return [len(c) for c in G.conjugacy_classes()]
    except Exception:
        pass
    
    if hasattr(G, 'elements'):
        elements = list(G.elements)
    else:
        elements = list(G)
        
    sizes = []
    seen = []
    for x in elements:
        if x not in seen:
            c = []
            for g in elements:
                try:
                    inv_g = g**-1
                except Exception:
                    inv_g = ~g
                conj = g * x * inv_g
                if conj not in c:
                    c.append(conj)
            sizes.append(len(c))
            for item in c:
                if item not in seen:
                    seen.append(item)
    return sizes

def is_power_of_p(n, p):
    if n < 1:
        return False
    if n == 1:
        return True
    if p <= 1:
        return False
    while n % p == 0:
        n = n // p
    return n == 1

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        G, p = witness
    except Exception:
        return [False, False]
    
    # H_1: p is a prime number
    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False
        
    # ¬Q: There exists a conjugacy class of G whose size is not a power of p
    try:
        sizes = get_conjugacy_class_sizes(G)
        neg_q_ok = False
        for s in sizes:
            if not is_power_of_p(s, p):
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: There exists a conjugacy class of G whose size is not a power of p"
]

N_HYP = 1
NEG_Q_INDEX = 1