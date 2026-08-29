import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _perm(n, k):
    """Helper to compute n P k, compatible with older Python versions."""
    if hasattr(math, 'perm'):
        return math.perm(n, k)
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // math.factorial(n - k)

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to provide the group G, and the integers k and n.
        G = witness[0]
        k = int(witness[1])
        n = int(witness[2])
    except Exception:
        return [False, False, False, False]

    # H_1: Let G be a finite group.
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: Let k be a positive integer such that k <= n.
    try:
        h2_ok = (k >= 1) and (k <= n)
    except Exception:
        h2_ok = False

    # H_3: Let G act sharply k-transitively on X.
    # We assume X is the natural domain of G, which has size G.degree.
    try:
        h3_ok = False
        if h1_ok and k >= 1:
            d = G.degree
            if k <= d:
                expected_order = _perm(d, k)
                # A group is sharply k-transitive if its order is exactly d P k
                # and it is k-transitive (has a single orbit of size d P k on k-tuples).
                if G.order() == expected_order:
                    start = tuple(range(k))
                    orbit = {start}
                    queue = [start]
                    gens = G.generators
                    for tup in queue:
                        for g in gens:
                            new_tup = tuple(g(i) for i in tup)
                            if new_tup not in orbit:
                                orbit.add(new_tup)
                                queue.append(new_tup)
                    if len(orbit) == expected_order:
                        h3_ok = True
    except Exception:
        h3_ok = False

    # ¬Q: The order of the group G is exactly n(n-1)...(n-k+1).
    # We want this to FAIL, so the negation must be TRUE.
    try:
        if k >= 1 and k <= n:
            expected_concl_order = _perm(n, k)
            neg_q_ok = G.order() != expected_concl_order
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: k is a positive integer such that k <= n",
    "H_3: G acts sharply k-transitively on X",
    "¬Q: The order of G is not exactly n(n-1)...(n-k+1)"
]

N_HYP = 3
NEG_Q_INDEX = 3