import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation())
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_valid_action(B, n, action_gens):
    if len(B.generators) != len(action_gens):
        return False
    if n < 0:
        return False
    id_B = B.identity
    id_X = Permutation([], size=n)
    
    mapping = {id_B: id_X}
    queue = [id_B]
    gens_B = B.generators
    gens_X = action_gens
    
    count = 0
    while queue:
        curr = queue.pop(0)
        curr_X = mapping[curr]
        for g_B, g_X in zip(gens_B, gens_X):
            nxt = curr * g_B
            nxt_X = curr_X * g_X
            if nxt in mapping:
                if mapping[nxt] != nxt_X:
                    return False
            else:
                mapping[nxt] = nxt_X
                queue.append(nxt)
        count += 1
        if count > 10000:
            return False
    return count == B.order()

def wreath_product_order(A, B, n, action_gens):
    d_A = A.degree
    if d_A == 0:
        d_A = 1
        
    gens_W = []
    
    for g in A.generators:
        for x in range(n):
            mapping = list(range(d_A * n))
            for y in range(d_A):
                try:
                    gy = g(y)
                except Exception:
                    gy = y
                mapping[x * d_A + y] = x * d_A + gy
            gens_W.append(Permutation(mapping))
            
    for h_X in action_gens:
        mapping = list(range(d_A * n))
        for x in range(n):
            try:
                hx = h_X(x)
            except Exception:
                hx = x
            for y in range(d_A):
                mapping[x * d_A + y] = hx * d_A + y
        gens_W.append(Permutation(mapping))
        
    if not gens_W:
        return 1
        
    W = PermutationGroup(gens_W)
    return W.order()

def conditions(witness) -> list[bool]:
    try:
        A, B, n, action_gens = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: A and B are groups
    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: B acts on a set X
    try:
        h2 = False
        if h1 and isinstance(n, int) and 0 <= n <= 100 and isinstance(action_gens, (list, tuple)):
            h2 = is_valid_action(B, n, action_gens)
    except Exception:
        h2 = False
        
    # H_3: A ≀_X B is the restricted wreath product of A by B over X
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False
        
    # ¬Q: A ≀_X B is not isomorphic to the external semidirect product A^(X) ⋊ B
    try:
        neg_q = False
        if h1 and h2 and h3:
            w_order = wreath_product_order(A, B, n, action_gens)
            expected_order = (A.order() ** n) * B.order()
            neg_q = (w_order != expected_order)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "H_2: B acts on a set X",
    "H_3: A ≀_X B is the restricted wreath product of A by B over X",
    "¬Q: A ≀_X B is not isomorphic to the external semidirect product A^(X) ⋊ B"
]

N_HYP = 3
NEG_Q_INDEX = 3