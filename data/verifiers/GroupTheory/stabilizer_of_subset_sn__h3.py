import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group acting on a finite set X of size n",
    "H_2: Y is a subset of X of size k",
    "¬Q: H is not isomorphic to the direct product S_k x S_{n-k}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            k = witness.get('k')
            H = witness.get('H')
        else:
            n, k, H = witness
    except Exception:
        return [False, False, False]

    # H_1: Let S_n be the symmetric group acting on a finite set X of size n
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    # H_2: Let Y be a subset of X of size k
    try:
        h2 = isinstance(k, int) and 0 <= k <= n and isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # ¬Q: H is not isomorphic to the direct product S_k x S_{n-k}
    try:
        target_order = math.factorial(k) * math.factorial(n - k)
        if H.order() != target_order:
            neg_q = True
        else:
            # Construct the direct product S_k x S_{n-k} embedded in S_n
            gens = []
            if k > 1:
                sk = SymmetricGroup(k)
                for g in sk.generators:
                    p = [g(i) for i in range(k)] + list(range(k, n))
                    gens.append(Permutation(p))
            if n - k > 1:
                snk = SymmetricGroup(n - k)
                for g in snk.generators:
                    p = list(range(k)) + [g(i) + k for i in range(n - k)]
                    gens.append(Permutation(p))
                    
            if not gens:
                target_group = PermutationGroup([Permutation(list(range(n)))])
            else:
                target_group = PermutationGroup(gens)
                
            if hasattr(H, 'is_isomorphic'):
                try:
                    neg_q = not H.is_isomorphic(target_group)
                except Exception:
                    # Fallback if is_isomorphic fails
                    H_orders = sorted([g.order() for g in H.elements])
                    target_orders = sorted([g.order() for g in target_group.elements])
                    neg_q = (H_orders != target_orders)
            else:
                H_orders = sorted([g.order() for g in H.elements])
                target_orders = sorted([g.order() for g in target_group.elements])
                neg_q = (H_orders != target_orders)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]