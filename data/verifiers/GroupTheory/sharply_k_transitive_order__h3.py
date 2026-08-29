import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math

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
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    'If a finite group G acts sharply k-transitively on a finite set X of size n,
    then the order of G is exactly n(n-1)...(n-k+1).'
    
    The conjecture is false because it omits the requirement that k <= n.
    If k > n, the set of k-tuples of distinct elements from X is empty,
    so ANY group acts sharply k-transitively on X (vacuously), but the formula
    gives an order of 0, which is impossible for a group.
    """
    try:
        # Witness can be (G, k) or (G, n, k) or (G, X, k)
        if len(witness) == 2:
            G, k = witness
            n = G.degree
        elif len(witness) == 3:
            G, X_or_n, k = witness
            if isinstance(X_or_n, (int, sympy.Integer)):
                n = X_or_n
            else:
                n = len(X_or_n)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'is_group') or hasattr(G, 'elements')
        if hasattr(G, 'order'):
            order = G.order()
            h1 = h1 and order > 0 and order < float('inf')
    except Exception:
        h1 = False

    # H_2: X is a finite set of size n
    try:
        n = int(n)
        h2 = n >= 0
    except Exception:
        h2 = False

    # H_3: G acts sharply k-transitively on X
    try:
        k = int(k)
        if not (h1 and h2 and k >= 0):
            h3 = False
        else:
            if G.order() > 10000:
                # Prevent timeout on unreasonably large groups
                h3 = False
            else:
                tuples = list(itertools.permutations(range(n), k))
                h3 = True
                elements = list(G.elements)
                for t1 in tuples:
                    for t2 in tuples:
                        count = 0
                        for g in elements:
                            # Check if permutation g maps tuple t1 to tuple t2
                            if all(g(t1[i]) == t2[i] for i in range(k)):
                                count += 1
                        if count != 1:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # ¬Q: The order of G is not exactly n(n-1)...(n-k+1)
    try:
        k = int(k)
        n = int(n)
        if k < 0 or n < 0:
            neg_q = False
        else:
            expected_order = math.perm(n, k)
            actual_order = int(G.order())
            neg_q = (actual_order != expected_order)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set of size n",
    "H_3: G acts sharply k-transitively on X",
    "¬Q: The order of G is not exactly n(n-1)...(n-k+1)"
]

N_HYP = 3
NEG_Q_INDEX = 3