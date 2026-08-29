import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy import eye, zeros
from sympy.ntheory import isprime

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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: The order of G is pm",
    "H_4: p > m",
    "¬Q: The Sylow p-subgroup of G is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        G, p, m = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: The order of G is pm
    try:
        order = G.order() if callable(G.order) else G.order
        h3 = bool(order == p * m)
    except Exception:
        h3 = False

    # H_4: p > m
    try:
        h4 = bool(p > m)
    except Exception:
        h4 = False

    # ¬Q: The Sylow p-subgroup of G is not a normal subgroup of G
    try:
        order = G.order() if callable(G.order) else G.order
        if order % p != 0:
            # If p does not divide the order of G, the Sylow p-subgroup is the trivial group,
            # which is always a normal subgroup. Thus, it is NOT "not normal".
            neg_q = False
        else:
            H = G.sylow_subgroup(p)
            is_normal = True
            if hasattr(G, 'is_normal'):
                is_normal = G.is_normal(H)
            else:
                # Fallback normality check: g * h * g^-1 in H for all generators
                for g in G.generators:
                    for h in H.generators:
                        if (g * h * g**-1) not in H:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]