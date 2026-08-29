import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    """
    Checks the hypotheses and negated conclusion for the Suborbit Rank Theorem.
    The dropped hypothesis is "x \in X".
    Witness is expected to be a tuple: (G, X, x)
    where G is a PermutationGroup, X is a list/set of integers, and x is an integer.
    """
    try:
        if not (isinstance(witness, tuple) and len(witness) == 3):
            return [False, False, False, False]
        G, X, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        if not hasattr(G, 'generators'):
            h1 = False
        else:
            X_set = set(X)
            # Check if X is closed under the action of G
            h1 = all(g(y) in X_set for g in G.generators for y in X_set)
    except Exception:
        h1 = False

    # H_2: The action of G on X is transitive
    try:
        if not h1 or not X_set:
            h2 = False
        else:
            elem = next(iter(X_set))
            orbit = set([elem])
            queue = [elem]
            while queue:
                curr = queue.pop(0)
                for g in G.generators:
                    nxt = g(curr)
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            h2 = (orbit == X_set)
    except Exception:
        h2 = False

    # H_3: G acts on X \times X diagonally
    try:
        # If G acts on X, the diagonal action on X \times X is naturally well-defined.
        h3 = h1
    except Exception:
        h3 = False

    # ¬Q: The number of orbits of G on X \times X is not equal to the number of orbits of G_x on X
    try:
        if not h1:
            neg_q = False
        else:
            X_set = set(X)
            
            # Compute the number of orbits of G on X \times X
            X_X = [(y, z) for y in X_set for z in X_set]
            unvisited_XX = set(X_X)
            G_orbits_XX = 0
            while unvisited_XX:
                start = unvisited_XX.pop()
                G_orbits_XX += 1
                queue = [start]
                while queue:
                    curr_y, curr_z = queue.pop(0)
                    for g in G.generators:
                        nxt = (g(curr_y), g(curr_z))
                        if nxt in unvisited_XX:
                            unvisited_XX.remove(nxt)
                            queue.append(nxt)
            
            # Compute G_x (stabilizer of x in G)
            if hasattr(G, 'domain') and x in G.domain:
                Gx_gens = G.stabilizer(x).generators
            else:
                # If x is not in the domain of G, it is fixed by all elements of G
                Gx_gens = G.generators
                
            # Compute the number of orbits of G_x on X
            unvisited_X = set(X_set)
            Gx_orbits_X = 0
            while unvisited_X:
                start = unvisited_X.pop()
                Gx_orbits_X += 1
                queue = [start]
                while queue:
                    curr = queue.pop(0)
                    for g in Gx_gens:
                        nxt = g(curr)
                        if nxt in unvisited_X:
                            unvisited_X.remove(nxt)
                            queue.append(nxt)
                            
            neg_q = (G_orbits_XX != Gx_orbits_X)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: The action of G on X is transitive",
    "H_3: G acts on X \\times X diagonally",
    "¬Q: The number of orbits of G on X \\times X is not equal to the number of orbits of G_x on X"
]

N_HYP = 3
NEG_Q_INDEX = 3