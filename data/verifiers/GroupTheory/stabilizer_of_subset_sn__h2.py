import itertools
import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
        # Witness can be (n, k, Y) or (n, Y)
        if len(witness) == 3:
            n, k, Y = witness
        elif len(witness) == 2:
            n, Y = witness
            if isinstance(Y, (set, frozenset, list, tuple)):
                k = len(Y)
            else:
                k = 1
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: S_n is the symmetric group acting on a finite set X of size n
    try:
        # Restrict n to a reasonable size to ensure fast execution (n! <= 40320)
        h1 = isinstance(n, int) and 1 <= n <= 8
    except Exception:
        h1 = False

    # H2: H is the setwise stabilizer of Y in S_n
    try:
        def is_valid_obj(obj, n_val):
            if isinstance(obj, int):
                return 0 <= obj < n_val
            elif isinstance(obj, (list, tuple, set, frozenset)):
                return all(is_valid_obj(x, n_val) for x in obj)
            return False
            
        h2 = isinstance(k, int) and 0 <= k <= n and is_valid_obj(Y, n)
    except Exception:
        h2 = False

    # neg_Q: H is NOT isomorphic to S_k \times S_{n-k}
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            def apply_perm(p_tup, obj):
                if isinstance(obj, int):
                    return p_tup[obj]
                elif isinstance(obj, (list, tuple)):
                    return type(obj)(apply_perm(p_tup, x) for x in obj)
                elif isinstance(obj, (set, frozenset)):
                    return frozenset(apply_perm(p_tup, x) for x in obj)
                else:
                    return obj

            # Find all permutations in S_n that stabilize Y
            H_perms = []
            for p_tup in itertools.permutations(range(n)):
                if apply_perm(p_tup, Y) == Y:
                    H_perms.append(Permutation(list(p_tup)))

            # Find all permutations in S_n that belong to S_k x S_{n-k}
            # This is exactly the setwise stabilizer of {0, 1, ..., k-1}
            Q_perms = []
            target_set = set(range(k))
            for p_tup in itertools.permutations(range(n)):
                if set(p_tup[i] for i in target_set) == target_set:
                    Q_perms.append(Permutation(list(p_tup)))

            # Check for isomorphism
            if len(H_perms) != len(Q_perms):
                neg_q = True
            else:
                H_orders = sorted([p.order() for p in H_perms])
                Q_orders = sorted([p.order() for p in Q_perms])
                if H_orders != Q_orders:
                    neg_q = True
                else:
                    # If orders and element orders match, use SymPy's abstract isomorphism check
                    H_group = PermutationGroup(H_perms)
                    Q_group = PermutationGroup(Q_perms)
                    neg_q = not H_group.is_isomorphic(Q_group)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group acting on a finite set X of size n",
    "H_2: H is the setwise stabilizer of Y in S_n",
    "¬Q: H is NOT isomorphic to the direct product S_k \\times S_{n-k}"
]

N_HYP = 2
NEG_Q_INDEX = 2