import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime, factorint

# Top-level setup for potential witness expressions
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

def conditions(witness):
    try:
        G, p, P, x = witness
    except Exception:
        return [False] * 5
        
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    try:
        if not isinstance(P, PermutationGroup):
            h2 = False
        else:
            is_sub = all(G.contains(g) for g in P.generators)
            if not is_sub:
                h2 = False
            else:
                order_G = G.order()
                k = factorint(order_G).get(p, 0) if order_G > 0 else 0
                h2 = bool(P.order() == p**k)
    except Exception:
        h2 = False
        
    try:
        if not G.contains(x):
            h3 = False
        else:
            h3 = bool(all(P.contains(x * g * ~x) for g in P.generators))
    except Exception:
        h3 = False
        
    try:
        order_x = x.order()
        if order_x == 1:
            h4 = True
        else:
            factors = factorint(order_x)
            h4 = bool(list(factors.keys()) == [p])
    except Exception:
        h4 = False
        
    try:
        neg_q = not bool(P.contains(x))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: x is an element of the normalizer N_G(P)",
    "H_4: The order of x is a power of p",
    "¬Q: The element x does not belong to P"
]

N_HYP = 4
NEG_Q_INDEX = 4