import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            p = witness['p']
            P = witness['P']
            Q = witness['Q']
        else:
            G, p, P, Q = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group (and P, Q are valid subgroups of G)
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(P, PermutationGroup) and 
              isinstance(Q, PermutationGroup) and 
              all(G.contains(x) for x in P.generators) and 
              all(G.contains(x) for x in Q.generators))
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # ¬Q: P and Q are NOT conjugate in G
    try:
        if not h1:
            neg_q = False
        else:
            are_conj = False
            if P.order() == Q.order():
                for g in G.generate():
                    # Check if g * P * g^-1 is a subset of Q
                    # Since orders are equal, subset implies equality
                    if all(Q.contains(g * x * ~g) for x in P.generators):
                        are_conj = True
                        break
            neg_q = not are_conj
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group (and P, Q are subgroups of G)",
    "H_2: p is a prime number",
    "¬Q: P and Q are not conjugate in G"
]

N_HYP = 2
NEG_Q_INDEX = 2