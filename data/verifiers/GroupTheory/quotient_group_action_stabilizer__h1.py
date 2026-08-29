import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness):
    try:
        G = witness.G
        N = witness.N
        X = witness.X
        x = witness.x
        action_G = witness.action_G
        action_G_mod_N = witness.action_G_mod_N
    except AttributeError:
        return [False, False, False, False, False]

    try:
        elements_G = list(G.elements)
        elements_N = list(N.elements)
        identity = G.identity
    except Exception:
        return [False, False, False, False, False]

    # H1: N is a normal subgroup of G
    try:
        h1 = True
        if identity not in elements_N:
            h1 = False
        for n1 in elements_N:
            if n1 not in elements_G:
                h1 = False
            for n2 in elements_N:
                if (n1 * n2) not in elements_N:
                    h1 = False
        for g in elements_G:
            inv_g = None
            for cand in elements_G:
                if (g * cand) == identity and (cand * g) == identity:
                    inv_g = cand
                    break
            if inv_g is None:
                h1 = False
            else:
                for n in elements_N:
                    if (g * n * inv_g) not in elements_N:
                        h1 = False
    except Exception:
        h1 = False

    # H2: N acts trivially on X
    try:
        h2 = True
        for n in elements_N:
            for y in X:
                if action_G(n, y) != y:
                    h2 = False
                    break
            if not h2: break
    except Exception:
        h2 = False

    # H3: G/N acts on X via the induced action (gN) \cdot x = g \cdot x
    try:
        h3 = True
        # Check if action_G_mod_N is well-defined on left cosets
        for g in elements_G:
            for n in elements_N:
                gn = g * n
                for y in X:
                    if action_G_mod_N(gn, y) != action_G_mod_N(g, y):
                        h3 = False
        # Check if it's a valid group action of G/N on X
        for y in X:
            if action_G_mod_N(identity, y) != y:
                h3 = False
        for g1 in elements_G:
            for g2 in elements_G:
                g1g2 = g1 * g2
                for y in X:
                    if action_G_mod_N(g1g2, y) != action_G_mod_N(g1, action_G_mod_N(g2, y)):
                        h3 = False
        # Check if the induced action matches action_G for the specific element x
        for g in elements_G:
            if action_G_mod_N(g, x) != action_G(g, x):
                h3 = False
    except Exception:
        h3 = False

    # H4: x is an element of X
    try:
        h4 = x in X
    except Exception:
        h4 = False

    # Negated Conclusion: The stabilizer of x in G/N is the quotient group G_x/N, where G_x is the stabilizer of x in G.
    try:
        G_x = [g for g in elements_G if action_G(g, x) == x]
        G_x_N = set()
        for g in G_x:
            for n in elements_N:
                G_x_N.add(g * n)
        
        S_set = set([g for g in elements_G if action_G_mod_N(g, x) == x])
        
        neg_q = (S_set != G_x_N)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N acts trivially on X",
    "H_3: G/N acts on X via the induced action",
    "H_4: x is an element of X",
    "¬Q: The stabilizer of x in G/N is not the quotient group G_x/N"
]

N_HYP = 4
NEG_Q_INDEX = 4