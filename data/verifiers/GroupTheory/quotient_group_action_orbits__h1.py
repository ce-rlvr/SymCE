import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    elif hasattr(group, 'generate'):
        return list(group.generate())
    else:
        return list(group)

def conditions(witness):
    try:
        G, N, X, op = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        G_elems = get_elements(G)
        N_elems = get_elements(N)
        
        h1 = True
        for n in N_elems:
            if n not in G_elems:
                h1 = False
                break
        
        if h1:
            for g in G_elems:
                g_inv = g**-1
                for n in N_elems:
                    if (g * n * g_inv) not in N_elems:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: X/N is the set of orbits of N on X (implies N acts on X)
    try:
        h2 = True
        e = G.identity
        for x in X:
            res = op(e, x)
            if res not in X or res != x:
                h2 = False
                break
                
        if h2:
            for n1 in N_elems:
                for n2 in N_elems:
                    for x in X:
                        res2 = op(n2, x)
                        if res2 not in X:
                            h2 = False
                            break
                        res1 = op(n1, res2)
                        res12 = op(n1 * n2, x)
                        if res1 not in X or res12 not in X or res1 != res12:
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # neg_Q: The operation is not well-defined or does not form a group action
    try:
        orbit_map = {}
        for x in X:
            orbit = set()
            for n in N_elems:
                res = op(n, x)
                orbit.add(res)
            orbit_map[x] = frozenset(orbit)
            
        well_defined = True
        for g1 in G_elems:
            for g2 in G_elems:
                g1N = frozenset({g1 * n for n in N_elems})
                g2N = frozenset({g2 * n for n in N_elems})
                if g1N == g2N:
                    for x1 in X:
                        for x2 in X:
                            if orbit_map[x1] == orbit_map[x2]:
                                res1 = op(g1, x1)
                                res2 = op(g2, x2)
                                if res1 not in X or res2 not in X:
                                    well_defined = False
                                    break
                                if orbit_map[res1] != orbit_map[res2]:
                                    well_defined = False
                                    break
                        if not well_defined: break
                if not well_defined: break
            if not well_defined: break

        is_action = True
        if well_defined:
            e = G.identity
            for x in X:
                res = op(e, x)
                if res not in X or orbit_map[res] != orbit_map[x]:
                    is_action = False
                    break
            if is_action:
                for g1 in G_elems:
                    for g2 in G_elems:
                        for x in X:
                            res_inner = op(g2, x)
                            if res_inner not in X:
                                is_action = False
                                break
                            res1 = op(g1, res_inner)
                            res2 = op(g1 * g2, x)
                            if res1 not in X or res2 not in X:
                                is_action = False
                                break
                            if orbit_map[res1] != orbit_map[res2]:
                                is_action = False
                                break
                        if not is_action: break
                    if not is_action: break

        neg_q = not (well_defined and is_action)
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: X/N is the set of orbits of N on X",
    "¬Q: The operation on X/N is not well-defined or does not form a group action"
]

N_HYP = 2
NEG_Q_INDEX = 2