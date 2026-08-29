import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Setup named objects
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

def conditions(witness):
    # Extract G, x, G_x
    G_x_provided = False
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, x, G_x = witness
                G_x_provided = True
            elif len(witness) == 2:
                G, x = witness
            else:
                G = witness[0]
                x = 0
        else:
            G = witness
            x = 0
    except Exception:
        return [False, False, False, False]

    h1 = False
    try:
        if isinstance(G, PermutationGroup) and G.is_transitive:
            h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if isinstance(G, PermutationGroup) and G.degree >= 2:
            h2 = True
    except Exception:
        pass

    h3 = False
    try:
        if isinstance(G, PermutationGroup):
            if not isinstance(x, int) or not (0 <= x < G.degree):
                h3 = False
            elif G_x_provided:
                if isinstance(G_x, PermutationGroup):
                    stab = G.stabilizer(x)
                    is_sub = True
                    for g in G_x.generators:
                        if not G.contains(g):
                            is_sub = False
                            break
                    if is_sub and G_x.order() == stab.order():
                        h3 = True
                        for g in G_x.generators:
                            if not stab.contains(g):
                                h3 = False
                                break
            else:
                G_x = G.stabilizer(x)
                h3 = True
    except Exception:
        pass

    neg_Q = False
    try:
        if h1 and h2 and h3:
            is_prim = bool(G.is_primitive())
            
            # Compute transversal using BFS to find one element mapping x to each y in the orbit
            id_perm = Permutation(size=G.degree)
            transversal = {x: id_perm}
            queue = [x]
            while queue:
                curr = queue.pop(0)
                for gen in G.generators:
                    nxt = gen(curr)
                    if nxt not in transversal:
                        transversal[nxt] = transversal[curr] * gen
                        queue.append(nxt)
            
            # Check if G_x is a maximal subgroup of G
            # G_x is maximal iff for all y != x, the subgroup <G_x, g_y> is G
            G_x_is_max = True
            if G_x.order() == G.order():
                G_x_is_max = False
            else:
                for y, g_y in transversal.items():
                    if y == x:
                        continue
                    gens = list(G_x.generators) + [g_y]
                    K = PermutationGroup(gens)
                    if K.order() < G.order():
                        G_x_is_max = False
                        break
            
            Q = (is_prim == G_x_is_max)
            neg_Q = not Q
    except Exception:
        pass

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a transitive permutation group acting on a set X",
    "H_2: X contains at least two elements",
    "H_3: G_x is the stabilizer subgroup of x in G",
    "¬Q: The action of G on X is primitive is NOT equivalent to G_x is a maximal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3