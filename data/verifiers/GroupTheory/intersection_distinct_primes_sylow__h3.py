import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            q = witness.get('q')
            P = witness.get('P')
            Q = witness.get('Q')
        else:
            G, p, q, P, Q = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p and q are distinct primes
    try:
        h2 = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h2 = False

    # H_3: Q is a Sylow q-subgroup of G
    try:
        if isinstance(Q, PermutationGroup) and isinstance(G, PermutationGroup):
            # Check if Q is a subgroup of G
            is_subgroup = all(g in G for g in Q.generators)
            if is_subgroup and isinstance(q, int) and q > 1:
                order_G = G.order()
                order_Q = Q.order()
                k = 0
                temp = order_G
                while temp % q == 0:
                    k += 1
                    temp //= q
                h3 = bool(order_Q == q**k)
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The intersection P \cap Q is not the trivial subgroup {1}
    try:
        if isinstance(P, PermutationGroup) and isinstance(Q, PermutationGroup):
            if P.order() < 5000 and Q.order() < 5000:
                def norm(perm):
                    arr = list(perm.array_form)
                    while arr and arr[-1] == len(arr) - 1:
                        arr.pop()
                    return tuple(arr)
                
                set_P = {norm(perm) for perm in P.generate_dimino()}
                set_Q = {norm(perm) for perm in Q.generate_dimino()}
                intersect = set_P.intersection(set_Q)
                intersect.discard(())  # Remove the identity element
                neg_q = len(intersect) > 0
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct primes",
    "H_3: Q is a Sylow q-subgroup of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup {1}"
]

N_HYP = 3
NEG_Q_INDEX = 3