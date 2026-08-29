import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def get_order(grp):
    order = grp.order
    if callable(order):
        return order()
    return order

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False] * 5
        G, p, P, Q = witness
    except Exception:
        return [False] * 5

    # H1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H2: p divides the order of G
    try:
        p_val = int(p)
        order_G = get_order(G)
        h2 = (order_G % p_val == 0)
    except Exception:
        h2 = False

    # H3: p^2 does not divide the order of G
    try:
        p_val = int(p)
        order_G = get_order(G)
        h3 = (order_G % (p_val**2) != 0)
    except Exception:
        h3 = False

    # H4: P and Q are distinct Sylow p-subgroups of G
    try:
        p_val = int(p)
        if p_val <= 1:
            h4 = False
        else:
            order_G = get_order(G)
            k = 0
            temp = order_G
            while temp % p_val == 0 and temp > 0:
                k += 1
                temp //= p_val
            sylow_order = p_val**k
            
            def is_subgroup(sub, super_group):
                return all(g in super_group for g in sub.generators)
            
            def group_eq(A, B):
                return is_subgroup(A, B) and is_subgroup(B, A)
            
            p_is_subgroup = is_subgroup(P, G)
            q_is_subgroup = is_subgroup(Q, G)
            
            h4 = (p_is_subgroup and q_is_subgroup and 
                  get_order(P) == sylow_order and get_order(Q) == sylow_order and 
                  not group_eq(P, Q))
    except Exception:
        h4 = False

    # neg_Q: P \cap Q is not the trivial subgroup {e}
    try:
        has_non_trivial = False
        identity = P.identity
        for i, g in enumerate(P.generate()):
            if i > 10000:  # Safety break for excessively large groups
                break
            if g != identity and g in Q:
                has_non_trivial = True
                break
        neg_q = has_non_trivial
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides the order of G",
    "H_3: p^2 does not divide the order of G",
    "H_4: P and Q are distinct Sylow p-subgroups of G",
    "¬Q: P \\cap Q is not the trivial subgroup {e}"
]

N_HYP = 4
NEG_Q_INDEX = 4