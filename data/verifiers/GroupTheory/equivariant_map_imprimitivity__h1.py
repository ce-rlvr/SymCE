import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G = witness['G']
        Y_action_gens = witness['Y_action_gens']
        phi = witness['phi']
    except Exception:
        return [False, False, False]
        
    if not isinstance(G, PermutationGroup):
        return [False, False, False]
        
    try:
        max_order = G.order()
        if max_order > 2000:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G acts on a set Y
    try:
        Y_size = max(phi) + 1 if phi else 0
        if Y_action_gens:
            Y_size = max(Y_size, max(p.size for p in Y_action_gens))
        
        padded_Y_gens = [Permutation(p.array_form, size=Y_size) for p in Y_action_gens]
        
        if len(G.generators) != len(padded_Y_gens):
            h1 = False
        else:
            gen_map = dict(zip(G.generators, padded_Y_gens))
            action = {G.identity: Permutation(size=Y_size)}
            queue = [G.identity]
            h1 = True
            while queue:
                curr = queue.pop(0)
                curr_Y = action[curr]
                for g, g_Y in gen_map.items():
                    nxt = curr * g
                    nxt_Y = curr_Y * g_Y
                    if nxt not in action:
                        action[nxt] = nxt_Y
                        queue.append(nxt)
                    else:
                        if action[nxt] != nxt_Y:
                            h1 = False
                            break
                if not h1:
                    break
            if h1:
                h1 = (len(action) == max_order)
    except Exception:
        h1 = False

    # H2: phi: X -> Y is a G-equivariant map
    try:
        if len(phi) != G.degree:
            h2 = False
        else:
            h2 = True
            gen_map = dict(zip(G.generators, padded_Y_gens))
            for g, g_Y in gen_map.items():
                for x in range(G.degree):
                    gx = g(x)
                    gy_phix = g_Y(phi[x])
                    if phi[gx] != gy_phix:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The set of non-empty fibers does not form a system of imprimitivity
    try:
        fibers = {}
        for x, y in enumerate(phi):
            if y not in fibers:
                fibers[y] = set()
            fibers[y].add(x)
        partition = list(fibers.values())
        
        is_sys = True
        if not G.is_transitive():
            is_sys = False
        else:
            for g in G.generators:
                for block in partition:
                    mapped_block = set(g(x) for x in block)
                    if mapped_block not in partition:
                        is_sys = False
                        break
                if not is_sys:
                    break
        neg_q = not is_sys
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G acts on a set Y",
    "H_2: phi: X -> Y is a G-equivariant map",
    "¬Q: The set of non-empty fibers does not form a system of imprimitivity for the action of G on X"
]

N_HYP = 2
NEG_Q_INDEX = 2