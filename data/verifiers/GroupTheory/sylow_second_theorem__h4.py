import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings that the witness expression may reference
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
        if len(witness) != 4:
            return [False, False, False, False]
        G, p, P, Q = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        elif not isinstance(G, PermutationGroup):
            h3 = False
        else:
            is_sub = all(g in G for g in P.generators)
            if not is_sub:
                h3 = False
            else:
                if not isinstance(p, (int, sympy.Integer)) or p < 2:
                    h3 = False
                else:
                    n = G.order()
                    ans = 1
                    while n % (ans * p) == 0:
                        ans *= p
                    h3 = (P.order() == ans)
    except Exception:
        h3 = False
        
    # ¬Q: There does not exist g in G such that Q = gPg^(-1)
    try:
        if isinstance(Q, PermutationGroup):
            Q_elems = set(Q.generate())
        else:
            Q_elems = set(Q)
    except Exception:
        Q_elems = None

    try:
        if Q_elems is None:
            neg_q = True
        elif not isinstance(G, PermutationGroup) or not isinstance(P, PermutationGroup):
            neg_q = True
        else:
            P_elems = list(P.generate())
            if len(P_elems) != len(Q_elems):
                neg_q = True
            else:
                is_conj = False
                for g in G.generate():
                    conj_P = set(g * h * ~g for h in P_elems)
                    if conj_P == Q_elems:
                        is_conj = True
                        break
                neg_q = not is_conj
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: There does not exist g in G such that Q = gPg^(-1)"
]

N_HYP = 3
NEG_Q_INDEX = 3