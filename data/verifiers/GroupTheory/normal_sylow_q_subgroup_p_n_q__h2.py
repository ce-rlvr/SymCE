import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            q = witness.get('q')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, p, q, n = witness
            else:
                return [False, False, False, False]
        elif hasattr(witness, 'G') and hasattr(witness, 'p') and hasattr(witness, 'q') and hasattr(witness, 'n'):
            G = witness.G
            p = witness.p
            q = witness.q
            n = witness.n
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = False
        if hasattr(G, 'order'):
            order = G.order()
            if order > 0 and order < float('inf'):
                h1 = True
    except Exception:
        h1 = False

    # H_2: n is a positive integer such that p^n < q
    try:
        h2 = (int(n) == n) and (n > 0) and (p**n < q)
    except Exception:
        h2 = False

    # H_3: The order of G is p^n q
    try:
        h3 = G.order() == (p**n * q)
    except Exception:
        h3 = False

    # ¬Q: The Sylow q-subgroup of G is not a normal subgroup of G
    try:
        if not isprime(q):
            # If q is not prime, the Sylow q-subgroup is undefined.
            # Thus the statement "The Sylow q-subgroup is normal" is false, making its negation true.
            neg_q = True
        else:
            Sq = G.sylow_subgroup(q)
            neg_q = not G.is_normal(Sq)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: n is a positive integer such that p^n < q",
    "H_3: The order of G is p^n q",
    "¬Q: The Sylow q-subgroup of G is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3