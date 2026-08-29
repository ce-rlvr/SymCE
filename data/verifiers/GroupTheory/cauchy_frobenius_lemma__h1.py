import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # default extraction
    G = None
    X = None
    action = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, X, action = witness
        elif isinstance(witness, list) and all(hasattr(g, '__call__') for g in witness):
            G = witness
            degree = 0
            for g in G:
                if hasattr(g, 'size'):
                    degree = max(degree, g.size)
            if degree > 0:
                X = list(range(degree))
            else:
                X = [0]
            action = lambda g, x: g(x)
        else:
            G = witness
            X = [0]
            action = lambda g, x: 0
    except Exception:
        return [False, False, False]

    # H_1: X is a finite set
    try:
        X_list = list(X)
        h1 = True
    except Exception:
        h1 = False

    # H_2: G acts on X
    h2 = False
    try:
        if h1:
            has_identity = False
            op = lambda a, b: a * b
            test_elements = []
            gens = []
            e = None
            
            if G == sympy.S.Integers:
                e = 0
                has_identity = True
                test_elements = [0, 1, -1, 2, -2]
                gens = [1, -1]
                op = lambda a, b: a + b
            else:
                if hasattr(G, 'identity'):
                    e = G.identity
                    has_identity = True
                elif hasattr(G, 'id'):
                    e = G.id
                    has_identity = True
                elif isinstance(G, (list, set, tuple)):
                    for g in G:
                        is_id = True
                        for x in X_list:
                            try:
                                if action(g, x) != x:
                                    is_id = False
                                    break
                            except Exception:
                                is_id = False
                                break
                        if is_id:
                            e = g
                            has_identity = True
                            break
                
                if hasattr(G, 'generators'):
                    gens = list(G.generators)
                    test_elements = gens + [g**-1 for g in gens if hasattr(g, '__pow__')]
                elif hasattr(G, '__iter__'):
                    test_elements = list(G)[:10]
                    gens = list(G)
            
            if has_identity:
                id_acts_trivially = True
                for x in X_list:
                    if action(e, x) != x:
                        id_acts_trivially = False
                        break
                
                if id_acts_trivially:
                    compat = True
                    for g in test_elements:
                        for h in test_elements:
                            try:
                                gh = op(g, h)
                            except Exception:
                                compat = False
                                break
                            for x in X_list:
                                try:
                                    if action(g, action(h, x)) != action(gh, x):
                                        compat = False
                                        break
                                except Exception:
                                    compat = False
                                    break
                            if not compat:
                                break
                        if not compat:
                            break
                    
                    is_group = True
                    if isinstance(G, (list, set, tuple)):
                        G_list = list(G)
                        for g in G_list:
                            for h in G_list:
                                try:
                                    gh = op(g, h)
                                    if gh not in G_list:
                                        is_group = False
                                        break
                                except Exception:
                                    is_group = False
                                    break
                            if not is_group:
                                break
                        if is_group:
                            for g in G_list:
                                found_inv = False
                                try:
                                    if g**-1 in G_list:
                                        found_inv = True
                                except Exception:
                                    pass
                                if not found_inv:
                                    for inv in G_list:
                                        try:
                                            if op(g, inv) == e and op(inv, g) == e:
                                                found_inv = True
                                                break
                                        except Exception:
                                            pass
                                if not found_inv:
                                    is_group = False
                                    break
                    
                    if compat and is_group:
                        h2 = True
    except Exception:
        h2 = False

    # neg_Q
    neg_q = False
    try:
        if h1 and h2:
            visited_indices = set()
            num_orbits = 0
            for i, x in enumerate(X_list):
                if i not in visited_indices:
                    num_orbits += 1
                    queue = [x]
                    visited_indices.add(i)
                    while queue:
                        curr = queue.pop(0)
                        for g in gens:
                            try:
                                nxt = action(g, curr)
                                nxt_idx = X_list.index(nxt)
                                if nxt_idx not in visited_indices:
                                    visited_indices.add(nxt_idx)
                                    queue.append(nxt)
                            except Exception:
                                pass
                            if G != sympy.S.Integers:
                                try:
                                    nxt_inv = action(g**-1, curr)
                                    nxt_inv_idx = X_list.index(nxt_inv)
                                    if nxt_inv_idx not in visited_indices:
                                        visited_indices.add(nxt_inv_idx)
                                        queue.append(nxt_inv)
                                except Exception:
                                    pass
            
            is_finite = False
            order = None
            if G == sympy.S.Integers:
                is_finite = False
            else:
                try:
                    if hasattr(G, 'order'):
                        order = G.order()
                        if order != sympy.oo:
                            is_finite = True
                    elif hasattr(G, '__len__'):
                        order = len(G)
                        is_finite = True
                except Exception:
                    pass
                
            rhs_value = None
            if is_finite and order is not None and order > 0:
                fixed_sum = 0
                if hasattr(G, 'generate'):
                    elements = list(G.generate())
                elif hasattr(G, 'elements'):
                    elements = list(G.elements)
                else:
                    elements = list(G)
                    
                for g in elements:
                    for x in X_list:
                        try:
                            if action(g, x) == x:
                                fixed_sum += 1
                        except Exception:
                            pass
                rhs_value = fixed_sum / order
                
            if rhs_value is None or abs(float(rhs_value) - num_orbits) > 1e-9:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a finite set",
    "H_2: G acts on X",
    "¬Q: The number of distinct orbits of the action is not equal to (1/|G|) * sum_{g in G} |X^g|"
]

N_HYP = 2
NEG_Q_INDEX = 2