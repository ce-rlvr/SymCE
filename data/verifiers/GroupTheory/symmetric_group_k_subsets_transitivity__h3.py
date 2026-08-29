import math
from sympy.combinatorics import SymmetricGroup, PermutationGroup, Permutation, AlternatingGroup
from sympy.combinatorics.named_groups import DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    n, k, S_n, X = None, None, None, None
    
    if isinstance(witness, dict):
        n = witness.get('n')
        k = witness.get('k')
        S_n = witness.get('S_n')
        X = witness.get('X')
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            n, k, S_n, X = witness
        elif len(witness) == 3:
            n, k, X = witness
    else:
        n = getattr(witness, 'n', None)
        k = getattr(witness, 'k', None)
        S_n = getattr(witness, 'S_n', None)
        X = getattr(witness, 'X', None)
        
    if S_n is None and n is not None:
        try:
            if n > 0:
                S_n = SymmetricGroup(n)
            elif n == 0:
                S_n = PermutationGroup(Permutation())
        except Exception:
            pass

    # H_1: n and k are integers with 0 <= k <= n
    h1 = False
    try:
        if isinstance(n, int) and isinstance(k, int):
            if 0 <= k <= n:
                h1 = True
    except Exception:
        pass

    # H_2: S_n is the symmetric group of degree n
    h2 = False
    try:
        if hasattr(S_n, 'order') and S_n.order() == math.factorial(n):
            if hasattr(S_n, 'degree') and S_n.degree == n:
                h2 = True
            elif n <= 1:
                h2 = True
    except Exception:
        pass

    # neg_Q: The natural induced action of S_n on X is NOT transitive
    neg_q = False
    try:
        canonical_X = set()
        if X is not None:
            for x in X:
                if isinstance(x, (set, frozenset)):
                    canonical_X.add(frozenset(x))
                elif isinstance(x, (tuple, list)):
                    canonical_X.add(tuple(x))
                else:
                    canonical_X.add(x)
        
        if not canonical_X:
            neg_q = True
        else:
            start = next(iter(canonical_X))
            orbit = set([start])
            queue = [start]
            gens = S_n.generators if hasattr(S_n, 'generators') else []
            
            def apply_g(g, x):
                if isinstance(x, (int, float)):
                    try:
                        return g(int(x))
                    except Exception:
                        return x
                elif isinstance(x, (set, frozenset)):
                    return frozenset(apply_g(g, i) for i in x)
                elif isinstance(x, (tuple, list)):
                    return tuple(apply_g(g, i) for i in x)
                else:
                    return x
            
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    nxt = apply_g(g, curr)
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            
            if orbit != canonical_X:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n and k are integers with 0 <= k <= n",
    "H_2: S_n is the symmetric group of degree n",
    "¬Q: The natural induced action of S_n on X is not transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2