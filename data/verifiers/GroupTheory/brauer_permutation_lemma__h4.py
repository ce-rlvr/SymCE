import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, dict):
            A = witness.get("A")
            X_size = witness.get("X_size")
            Y_size = witness.get("Y_size")
            action_X = witness.get("action_X")
            action_Y = witness.get("action_Y")
        elif isinstance(witness, tuple) and len(witness) == 5:
            A, X_size, Y_size, action_X, action_Y = witness
        else:
            A, X_size, Y_size, action_X, action_Y = None, None, None, None, None
            
        if action_X is not None:
            action_X = [Permutation(p) if not isinstance(p, Permutation) else p for p in action_X]
        if action_Y is not None:
            action_Y = [Permutation(p) if not isinstance(p, Permutation) else p for p in action_Y]
    except Exception:
        A, X_size, Y_size, action_X, action_Y = None, None, None, None, None

    # H_1: A is a finite group
    try:
        h1 = isinstance(A, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X and Y are finite sets
    try:
        h2 = isinstance(X_size, int) and X_size >= 0 and isinstance(Y_size, int) and Y_size >= 0
    except Exception:
        h2 = False

    # H_3: A acts on both X and Y
    try:
        def perms_equal(p1, p2):
            s = max(p1.size, p2.size)
            for i in range(s):
                if p1(i) != p2(i):
                    return False
            return True

        def is_valid_action(A, size, images):
            if not isinstance(images, list): return False
            if len(A.generators) != len(images): return False
            for img in images:
                if not isinstance(img, Permutation): return False
                for i in range(size, img.size):
                    if img(i) != i:
                        return False
            
            if not A.generators:
                return True
                
            gen_img_pairs = list(zip(A.generators, images))
            id_img = images[0]**0
            mapping = {A.identity: id_img}
            queue = [A.identity]
            
            while queue:
                curr = queue.pop(0)
                curr_img = mapping[curr]
                for g, img_g in gen_img_pairs:
                    nxt = curr * g
                    nxt_img = curr_img * img_g
                    if nxt in mapping:
                        if not perms_equal(mapping[nxt], nxt_img):
                            return False
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
            return True

        h3 = False
        if h1 and h2:
            h3 = is_valid_action(A, X_size, action_X) and is_valid_action(A, Y_size, action_Y)
    except Exception:
        h3 = False

    # neg_Q: The number of orbits of A on X is not equal to the number of orbits of A on Y
    try:
        def num_orbits(size, images):
            parent = list(range(size))
            def find(i):
                if parent[i] == i: return i
                parent[i] = find(parent[i])
                return parent[i]
            def union(i, j):
                root_i = find(i)
                root_j = find(j)
                if root_i != root_j:
                    parent[root_i] = root_j
                    
            for img in images:
                for i in range(size):
                    j = img(i) if i < img.size else i
                    union(i, j)
                    
            orbits = set(find(i) for i in range(size))
            return len(orbits)

        neg_q = False
        if h1 and h2 and h3:
            orbits_X = num_orbits(X_size, action_X)
            orbits_Y = num_orbits(Y_size, action_Y)
            neg_q = orbits_X != orbits_Y
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a finite group",
    "H_2: X and Y are finite sets",
    "H_3: A acts on both X and Y",
    "¬Q: The number of orbits of A on X is not equal to the number of orbits of A on Y"
]

N_HYP = 3
NEG_Q_INDEX = 3