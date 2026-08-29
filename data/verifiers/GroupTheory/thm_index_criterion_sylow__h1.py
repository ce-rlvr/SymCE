import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a subgroup of G such that the order of P is a power of p",
    "H_3: p does not divide the index of P in G",
    "neg_Q: P is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            P = witness.get('P')
            p = witness.get('p')
        elif hasattr(witness, 'G') and hasattr(witness, 'P') and hasattr(witness, 'p'):
            G = witness.G
            P = witness.P
            p = witness.p
        elif isinstance(witness, tuple) and len(witness) >= 3:
            G = witness[0]
            P = witness[1]
            p = witness[2]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: P is a subgroup of G such that the order of P is a power of p
    try:
        is_sub = False
        if hasattr(P, 'is_subgroup'):
            is_sub = P.is_subgroup(G)
        elif hasattr(G, 'has_subgroup'):
            is_sub = G.has_subgroup(P)
        elif hasattr(P, 'generators') and hasattr(G, 'contains'):
            is_sub = all(G.contains(g) for g in P.generators)
        else:
            is_sub = True

        order_P = P.order()
        n = int(order_P)
        if n <= 0:
            is_pow = False
        else:
            while n % p == 0 and n > 1:
                n //= p
            is_pow = (n == 1)
        h2 = bool(is_sub and is_pow)
    except Exception:
        h2 = False

    # H_3: p does not divide the index of P in G
    try:
        if hasattr(G, 'index'):
            index = G.index(P)
        else:
            index = int(G.order()) // int(P.order())
        h3 = bool(index % p != 0)
    except Exception:
        h3 = False

    # neg_Q: P is not a Sylow p-subgroup of G
    try:
        if isinstance(witness, dict) and 'is_sylow' in witness:
            is_sylow = bool(witness['is_sylow'])
        elif hasattr(witness, 'is_sylow'):
            is_sylow = bool(witness.is_sylow)
        elif isinstance(witness, tuple) and len(witness) >= 4:
            is_sylow = bool(witness[3])
        elif hasattr(P, 'is_sylow_subgroup'):
            is_sylow = P.is_sylow_subgroup(G, p)
        elif hasattr(G, 'is_sylow_subgroup'):
            is_sylow = G.is_sylow_subgroup(P, p)
        else:
            order_G = int(G.order())
            order_P = int(P.order())
            count = 0
            while order_G % p == 0 and order_G > 0:
                count += 1
                order_G //= p
            is_sylow = (order_P == p ** count)
        neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]