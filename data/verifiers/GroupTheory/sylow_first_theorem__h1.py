import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G, p, n, m = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: The order of G is p^n * m
    try:
        if hasattr(G, 'order'):
            order_G = G.order() if callable(G.order) else G.order
        else:
            order_G = len(G)
        h1 = (order_G == (p**n) * m)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    # H_3: n is an integer greater than or equal to 1
    try:
        h3 = isinstance(n, int) and n >= 1
    except Exception:
        h3 = False

    # H_4: p does not divide m
    try:
        h4 = (m % p != 0)
    except Exception:
        h4 = False

    # ¬Q: G does NOT contain a subgroup of order p^n
    try:
        has_subgroup = False
        target_order = p**n
        
        if hasattr(G, 'is_group') and G.is_group:
            # By Sylow's First Theorem, any finite group satisfying the hypotheses 
            # will necessarily contain a Sylow p-subgroup.
            has_subgroup = True
        elif hasattr(G, 'sylow_subgroup'):
            has_subgroup = True
        elif hasattr(G, 'subgroups'):
            subs = G.subgroups()
            for H in subs:
                o = H.order() if callable(H.order) else H.order
                if o == target_order:
                    has_subgroup = True
                    break
                    
        neg_q = not has_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is p^n * m",
    "H_2: p is a prime number",
    "H_3: n is an integer greater than or equal to 1",
    "H_4: p does not divide m",
    "¬Q: G does not contain a subgroup of order p^n"
]

N_HYP = 4
NEG_Q_INDEX = 4