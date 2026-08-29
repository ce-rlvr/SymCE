import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 5:
            return [False] * 4 + [False]
        G, X, action, H, g = witness
    except Exception:
        return [False] * 4 + [False]

    # H_1: G is a permutation group, X is a list, H is a permutation group, g is a permutation
    try:
        h1 = (isinstance(G, sympy.combinatorics.PermutationGroup) and 
              isinstance(X, (list, tuple)) and 
              isinstance(H, sympy.combinatorics.PermutationGroup) and 
              isinstance(g, sympy.combinatorics.Permutation) and
              callable(action))
    except Exception:
        h1 = False

    # H_2: action is a valid group action of G on X
    try:
        h2 = True
        if h1:
            id_G = G.identity
            for x in X:
                if action(id_G, x) != x:
                    h2 = False
                    break
            if h2:
                if G.order() > 200:
                    h2 = False
                else:
                    elements = list(G.generate())
                    for a in elements:
                        for b in elements:
                            ab = a * b
                            for x in X:
                                if action(ab, x) != action(a, action(b, x)):
                                    h2 = False
                                    break
                            if not h2: break
                        if not h2: break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        if h1:
            h3 = all(gen in G for gen in H.generators)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: gHg^{-1} is a subgroup of G
    try:
        if h1:
            g_inv = ~g
            conj_gens = [g * h * g_inv for h in H.generators]
            gHg_inv = sympy.combinatorics.PermutationGroup(conj_gens)
            h4 = all(gen in G for gen in conj_gens)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: X^H and X^{gHg^{-1}} have different cardinalities
    try:
        if h1 and h2 and h3 and h4:
            fixed_H = 0
            for x in X:
                if all(action(h, x) == x for h in H.generate()):
                    fixed_H += 1
                    
            fixed_gHg = 0
            for x in X:
                if all(action(k, x) == x for k in gHg_inv.generate()):
                    fixed_gHg += 1
                    
            neg_q = (fixed_H != fixed_gHg)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group, X is a list, H is a permutation group, g is a permutation",
    "H_2: action is a valid group action of G on X",
    "H_3: H is a subgroup of G",
    "H_4: gHg^{-1} is a subgroup of G",
    "¬Q: X^H and X^{gHg^{-1}} have different cardinalities"
]

N_HYP = 4
NEG_Q_INDEX = 4