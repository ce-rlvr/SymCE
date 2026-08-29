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
                G, H, p = witness
            elif len(witness) == 2:
                G, H = witness
                p = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and G.order() < float('inf')
    except Exception:
        h1 = False

    # H_2: H is a finite group
    try:
        h2 = hasattr(H, 'order') and H.order() < float('inf')
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    try:
        # The theorem holds for all finite groups when p is a prime.
        # The dropped hypothesis is "p is a prime".
        # If p is composite, the definition of Sylow p-subgroup is invalid,
        # and the structural properties (like maximum p-power dividing the order) fail.
        if p is not None:
            if isprime(p):
                neg_q = False
            else:
                if G.order() == 1 and H.order() == 1:
                    neg_q = False
                else:
                    neg_q = True
        else:
            # If p is not provided, the conclusion fails if there exists a p that breaks it.
            # For any non-trivial groups, p = |G| * |H| will break the conclusion.
            if G.order() == 1 and H.order() == 1:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a finite group",
    "¬Q: The conclusion fails (p is not prime, causing Sylow properties to fail)"
]

N_HYP = 2
NEG_Q_INDEX = 2