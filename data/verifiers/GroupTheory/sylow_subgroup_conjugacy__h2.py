import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_sylow_subgroup(H, G):
    if not isinstance(H, PermutationGroup):
        return False
    if not H.is_subgroup(G):
        return False
    order_H = H.order()
    order_G = G.order()
    factors = factorint(order_H)
    if len(factors) > 1:
        return False
    if len(factors) == 1:
        p = list(factors.keys())[0]
        if (order_G // order_H) % p == 0:
            return False
        return True
    if len(factors) == 0:
        return True

def conditions(witness):
    try:
        G = witness[0]
        P = witness[1]
        Q = witness[2]
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: P and Q are Sylow p-subgroups of G
    # The conjecture is false because the hypothesis "for the same prime p" was dropped.
    # Thus, we check if P and Q are Sylow subgroups for potentially different primes.
    try:
        h2 = is_sylow_subgroup(P, G) and is_sylow_subgroup(Q, G)
    except Exception:
        h2 = False
        
    # neg_Q: P and Q are NOT conjugate
    try:
        if P.order() != Q.order():
            neg_q = True
        else:
            Q_elems = set(Q.generate())
            match_found = False
            for g in G.generate():
                match = True
                for x in P.generators:
                    try:
                        conj = g * x * ~g
                    except Exception:
                        match = False
                        break
                    if conj not in Q_elems:
                        match = False
                        break
                if match:
                    match_found = True
                    break
            neg_q = not match_found
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P and Q are Sylow p-subgroups of G",
    "¬Q: P and Q are not conjugate"
]

N_HYP = 2
NEG_Q_INDEX = 2