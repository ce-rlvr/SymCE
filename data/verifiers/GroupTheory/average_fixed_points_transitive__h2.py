import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    try:
        if isinstance(witness, tuple):
            G, X = witness
            X = list(set(X))
        else:
            G = witness
            X = list(range(G.degree))
            
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        elif not X:
            h2 = True
        else:
            orbit = set()
            x0 = X[0]
            queue = [x0]
            orbit.add(x0)
            while queue:
                curr = queue.pop(0)
                for gen in G.generators:
                    nxt = gen(curr)
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            h2 = (orbit == set(X))
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        elif not X:
            orbits = 0
            fixed_points_sum = orbits * G.order()
            neg_q = fixed_points_sum != G.order()
        else:
            unvisited = set(X)
            orbits = 0
            while unvisited:
                x = unvisited.pop()
                orbits += 1
                orbit_x = {x}
                queue = [x]
                while queue:
                    curr = queue.pop(0)
                    for gen in G.generators:
                        nxt = gen(curr)
                        if nxt not in orbit_x:
                            orbit_x.add(nxt)
                            queue.append(nxt)
                unvisited -= orbit_x
                
            fixed_points_sum = orbits * G.order()
            neg_q = fixed_points_sum != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G acts transitively on X",
    "¬Q: sum_{g in G} |X^g| != |G|"
]

N_HYP = 2
NEG_Q_INDEX = 2