import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint, isprime

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

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            p = witness.get('p')
            if p is None and G is not None and H is not None:
                try:
                    p = G.order() // H.order()
                except Exception:
                    pass
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, p = witness
            elif len(witness) == 2:
                G, H = witness
                try:
                    p = G.order() // H.order()
                except Exception:
                    p = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: p is the smallest prime number dividing the order of G
    try:
        if p is None or not isprime(p):
            h1_ok = False
        else:
            order_G = G.order()
            if order_G == sympy.oo:
                h1_ok = False
            else:
                factors = factorint(order_G)
                if factors:
                    smallest_prime = min(factors.keys())
                    h1_ok = bool(p == smallest_prime)
                else:
                    h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = bool(H.is_subgroup(G))
    except Exception:
        h2_ok = False

    # H_3: The index of H in G is equal to p
    try:
        order_G = G.order()
        order_H = H.order()
        if order_G == sympy.oo or order_H == sympy.oo:
            if hasattr(G, 'index'):
                h3_ok = bool(G.index(H) == p)
            else:
                h3_ok = False
        else:
            if order_G % order_H == 0:
                h3_ok = bool(order_G // order_H == p)
            else:
                h3_ok = False
    except Exception:
        h3_ok = False

    # neg_Q: H is NOT a normal subgroup of G
    try:
        neg_q_ok = not bool(H.is_normal(G))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is the smallest prime number dividing the order of G",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is equal to p",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3