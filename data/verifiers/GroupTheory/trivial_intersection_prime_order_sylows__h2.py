import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import symbols, Rational, Integer
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        G, p, P, Q = witness
    except Exception:
        return [False] * 5

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p divides the order of G
    try:
        p_val = int(p)
        h2 = p_val > 1 and G.order() % p_val == 0
    except Exception:
        h2 = False

    # H3: p^2 does not divide the order of G
    try:
        p_val = int(p)
        h3 = p_val > 1 and G.order() % (p_val**2) != 0
    except Exception:
        h3 = False

    # H4: P and Q are distinct Sylow p-subgroups of G
    try:
        p_val = int(p)
        if p_val > 1:
            # Find the highest power of p dividing the order of G
            k = 0
            while G.order() % (p_val**(k+1)) == 0:
                k += 1
            target_order = p_val**k
            
            P_is_sub = all(g in G for g in P.generators)
            Q_is_sub = all(g in G for g in Q.generators)
            P_order = P.order() == target_order
            Q_order = Q.order() == target_order
            
            # P and Q are distinct if P is not a subgroup of Q (since they have the same order)
            distinct = not all(g in Q for g in P.generators)
            
            h4 = P_is_sub and Q_is_sub and P_order and Q_order and distinct
        else:
            h4 = False
    except Exception:
        h4 = False

    # Negated Conclusion: P \cap Q is NOT the trivial subgroup {e}
    try:
        neg_q = False
        # If there is any non-identity element in both P and Q, the intersection is not trivial
        for g in P.generate():
            if g != g**2 and g in Q:  # g != g**2 is a universal check for non-identity elements
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p divides the order of G",
    "H_3: p^2 does not divide the order of G",
    "H_4: P and Q are distinct Sylow p-subgroups of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup {e}"
]

N_HYP = 4
NEG_Q_INDEX = 4