import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, p, P = witness
        elif len(witness) == 4:
            G, p, P, _ = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H3: P is a Sylow p-subgroup of G
    try:
        h3 = False
        if h1 and h2 and isinstance(P, PermutationGroup):
            is_sub = True
            for gen in P.generators:
                if gen not in G:
                    is_sub = False
                    break
            if is_sub:
                order_G = G.order()
                order_P = P.order()
                k = 0
                temp = order_G
                while temp > 0 and temp % p == 0:
                    k += 1
                    temp //= p
                if order_P == p**k:
                    h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: n_p does NOT divide [G:P]
    try:
        neg_q = False
        if h1 and h2 and h3:
            P_elements = set(P.elements)
            conjugates = set()
            for g in G.elements:
                conj = frozenset(~g * x * g for x in P_elements)
                conjugates.add(conj)
            n_p = len(conjugates)
            index = G.order() // P.order()
            if index % n_p != 0:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "not Q: n_p does not divide the index of P in G"
]

N_HYP = 3
NEG_Q_INDEX = 3