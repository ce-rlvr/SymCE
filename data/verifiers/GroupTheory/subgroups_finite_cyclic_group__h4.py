import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a cyclic group",
    "H_3: the order of G is n",
    "H_4: d divides n",
    "¬Q: G does not contain exactly one subgroup of order d"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        G, n, d = witness
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a cyclic group
    try:
        if not h1:
            h2 = False
        else:
            order = G.order() if callable(G.order) else G.order
            h2 = any((g.order() if callable(g.order) else g.order) == order for g in G.elements)
    except Exception:
        h2 = False

    # H_3: the order of G is n
    try:
        if not h1:
            h3 = False
        else:
            order = G.order() if callable(G.order) else G.order
            h3 = (order == n)
    except Exception:
        h3 = False

    # H_4: d divides n
    try:
        h4 = (n % d == 0)
    except Exception:
        h4 = False

    # ¬Q: G does not contain exactly one subgroup of order d
    try:
        if not h1:
            neg_q = False
        else:
            if d <= 0:
                # The order of a subgroup must be strictly positive.
                # Thus, there are 0 subgroups of order d <= 0.
                neg_q = True
            else:
                elements = list(G.elements)
                # Find the identity element
                identity = next(e for e in elements if e * e == e)
                
                # Generate all subgroups to count how many have order d
                subgroups = {frozenset([identity])}
                queue = [frozenset([identity])]
                
                while queue:
                    H = queue.pop(0)
                    for g in elements:
                        if g not in H:
                            # Generate the closure of H U {g}
                            closure = set(H)
                            closure.add(g)
                            q2 = [g]
                            while q2:
                                x = q2.pop()
                                for y in list(closure):
                                    xy = x * y
                                    if xy not in closure:
                                        closure.add(xy)
                                        q2.append(xy)
                                    yx = y * x
                                    if yx not in closure:
                                        closure.add(yx)
                                        q2.append(yx)
                            new_H = frozenset(closure)
                            if new_H not in subgroups:
                                subgroups.add(new_H)
                                queue.append(new_H)
                
                count = sum(1 for H in subgroups if len(H) == d)
                neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]