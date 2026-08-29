import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup
)

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
    # Extract G, p, m from the witness
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        G, p, m = witness
    elif isinstance(witness, dict):
        G = witness.get('G', witness)
        p = witness.get('p', None)
        m = witness.get('m', None)
    else:
        G = witness
        p, m = None, None

    # If p and m are not explicitly provided, try to deduce them from G's order
    # Since p > m and |G| = p * m, it must be that p^2 > |G|.
    if p is None or m is None:
        try:
            order = G.order()
            for prime in sympy.primefactors(order):
                if prime * prime > order:
                    p = prime
                    m = order // prime
                    break
        except Exception:
            pass

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: m is a positive integer
    try:
        h2 = isinstance(m, int) and m > 0
    except Exception:
        h2 = False

    # H_3: The order of G is pm
    try:
        h3 = bool(G.order() == p * m)
    except Exception:
        h3 = False

    # H_4: p > m
    try:
        h4 = bool(p > m)
    except Exception:
        h4 = False

    # ¬Q: The Sylow p-subgroup of G is NOT a normal subgroup of G
    try:
        H = G.sylow_subgroup(p)
        is_normal = True
        # Check if g^-1 * h * g is in H for all generators g of G and h of H
        for g in G.generators:
            for h in H.generators:
                if (~g * h * g) not in H:
                    is_normal = False
                    break
            if not is_normal:
                break
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: m is a positive integer",
    "H_3: The order of G is pm",
    "H_4: p > m",
    "¬Q: The Sylow p-subgroup of G is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4