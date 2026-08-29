import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3), Permutation(0, 3)(1, 2)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, dict):
            G_elems = list(witness['G'])
            N_elems = list(witness['N'])
            X = list(witness['X'])
            action = witness['action']
            mul = witness['mul']
            inv = witness['inv']
            e = witness['e']
        else:
            if len(witness) == 4:
                G, N, X, action = witness
                mul = lambda g1, g2: g1 * g2
            elif len(witness) == 2:
                G, N = witness
                X = list(G.domain) if hasattr(G, 'domain') else list(range(G.degree))
                action = lambda g, x: g(x)
                # SymPy permutations multiply left-to-right: (g1*g2)(x) = g2(g1(x)).
                # To form a valid left action, we use the opposite group operation.
                mul = lambda g1, g2: g2 * g1
            else:
                return [False, False, False]
                
            G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
            N_elems = list(N.elements) if hasattr(N, 'elements') else list(N)
            e = G.identity if hasattr(G, 'identity') else G_elems[0]**0
            inv = lambda g: g**-1

        # H_1: G is a group acting on a set X (Left Action)
        h1 = True
        for x in X:
            if action(e, x) != x:
                h1 = False
                break
        if h1:
            for g1 in G_elems:
                for g2 in G_elems:
                    for x in X:
                        if action(mul(g1, g2), x) != action(g1, action(g2, x)):
                            h1 = False
                            break
                    if not h1: break
                if not h1: break

        # H_2: N is a normal subgroup of G
        h2 = True
        try:
            N_set = set(N_elems)
        except TypeError:
            N_set = N_elems
            
        if e not in N_set:
            h2 = False
        if h2:
            for n1 in N_elems:
                for n2 in N_elems:
                    if mul(n1, n2) not in N_set:
                        h2 = False
                        break
                if not h2: break
        if h2:
            for n in N_elems:
                if inv(n) not in N_set:
                    h2 = False
                    break
        if h2:
            for g in G_elems:
                for n in N_elems:
                    # Check g * n * g^-1 in N
                    if mul(mul(g, n), inv(g)) not in N_set:
                        h2 = False
                        break
                if not h2: break

        # ¬Q: The operation is NOT well-defined OR does NOT form a group action
        orbit_map = {}
        for x in X:
            orb = frozenset(action(n, x) for n in N_elems)
            orbit_map[x] = orb

        well_defined = True
        for g1 in G_elems:
            for g2 in G_elems:
                # g1 N == g2 N iff g1^-1 * g2 in N
                if mul(inv(g1), g2) in N_set:
                    for x1 in X:
                        for x2 in X:
                            if orbit_map[x1] == orbit_map[x2]:
                                if orbit_map[action(g1, x1)] != orbit_map[action(g2, x2)]:
                                    well_defined = False
                                    break
                        if not well_defined: break
                if not well_defined: break
            if not well_defined: break

        is_action = True
        if well_defined:
            # Check identity: eN * (N*x) == N*x
            for x in X:
                if orbit_map[action(e, x)] != orbit_map[x]:
                    is_action = False
                    break
            
            # Check compatibility: (g1 N * g2 N) * (N*x) == g1 N * (g2 N * (N*x))
            if is_action:
                for g1 in G_elems:
                    for g2 in G_elems:
                        for x in X:
                            orb_left = orbit_map[action(mul(g1, g2), x)]
                            y = action(g2, x)
                            orb_right = orbit_map[action(g1, y)]
                            if orb_left != orb_right:
                                is_action = False
                                break
                        if not is_action: break
                    if not is_action: break

        neg_q = not (well_defined and is_action)

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N is a normal subgroup of G",
    "¬Q: The operation is not well-defined or does not form a group action"
]

N_HYP = 2
NEG_Q_INDEX = 2