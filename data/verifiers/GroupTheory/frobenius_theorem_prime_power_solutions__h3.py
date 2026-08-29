import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, p, e = witness
            elif len(witness) == 2:
                G, p = witness
                try:
                    e = G.identity
                except Exception:
                    e = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and getattr(G, 'is_finite', True)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: e is the identity element of G
    try:
        h3 = (e == G.identity)
    except Exception:
        h3 = False

    # ¬Q: The number of elements x \in G such that x^p = e is NOT a multiple of p
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            count = 0
            # Handle both property and method just in case of sympy version differences
            elements = G.elements() if callable(G.elements) else G.elements
            for x in elements:
                if x**p == e:
                    count += 1
            neg_q = (count % p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: e is the identity element of G",
    "¬Q: The number of elements x in G such that x^p = e is not a multiple of p"
]

N_HYP = 3
NEG_Q_INDEX = 3