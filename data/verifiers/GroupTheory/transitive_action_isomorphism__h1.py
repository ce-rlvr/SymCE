import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def get_val(w, key):
    if isinstance(w, dict):
        return w[key]
    return getattr(w, key)

def contains(iterable, item):
    for x in iterable:
        if x == item:
            return True
    return False

def conditions(witness):
    # H1: X is a set
    try:
        X = get_val(witness, 'X')
        if isinstance(X, str):
            h1 = False
        else:
            iter(X)
            h1 = True
    except Exception:
        h1 = False

    # H2: G acts transitively on X
    try:
        G = get_val(witness, 'G')
        X = get_val(witness, 'X')
        op = get_val(witness, 'op')
        action = get_val(witness, 'action')
        
        is_action = True
        for g1 in G:
            for g2 in G:
                g1g2 = op(g1, g2)
                if not contains(G, g1g2):
                    is_action = False
                    break
                for y in X:
                    if action(g1g2, y) != action(g1, action(g2, y)):
                        is_action = False
                        break
                if not is_action: break
            if not is_action: break
            
        is_transitive = True
        if is_action:
            for a in X:
                for b in X:
                    can_reach = False
                    for g in G:
                        if action(g, a) == b:
                            can_reach = True
                            break
                    if not can_reach:
                        is_transitive = False
                        break
                if not is_transitive: break
                
        h2 = is_action and is_transitive
    except Exception:
        h2 = False

    # H3: x \in X
    try:
        X = get_val(witness, 'X')
        x = get_val(witness, 'x')
        h3 = contains(X, x)
    except Exception:
        h3 = False

    # H4: H = Stab(x)
    try:
        G = get_val(witness, 'G')
        action = get_val(witness, 'action')
        x = get_val(witness, 'x')
        H = get_val(witness, 'H')
        
        expected_H = []
        for g in G:
            if action(g, x) == x:
                if not contains(expected_H, g):
                    expected_H.append(g)
                    
        h4 = True
        H_list = list(H)
        if len(H_list) != len(expected_H):
            h4 = False
        else:
            for h in H_list:
                if not contains(expected_H, h):
                    h4 = False
                    break
            if h4:
                for h in expected_H:
                    if not contains(H_list, h):
                        h4 = False
                        break
    except Exception:
        h4 = False

    # neg_Q: \phi(gH) = g.x is NOT a well-defined bijection
    try:
        G = get_val(witness, 'G')
        X = get_val(witness, 'X')
        op = get_val(witness, 'op')
        action = get_val(witness, 'action')
        x = get_val(witness, 'x')
        H = get_val(witness, 'H')
        
        def get_coset(g):
            coset = []
            for h in H:
                val = op(g, h)
                if not contains(coset, val):
                    coset.append(val)
            return coset
        
        def cosets_equal(c1, c2):
            if len(c1) != len(c2): return False
            for item in c1:
                if not contains(c2, item): return False
            return True

        cosets = []
        for g in G:
            cosets.append((g, get_coset(g)))
            
        is_well_defined = True
        for g1, c1 in cosets:
            for g2, c2 in cosets:
                if cosets_equal(c1, c2):
                    if action(g1, x) != action(g2, x):
                        is_well_defined = False
                        break
            if not is_well_defined: break
            
        is_injective = True
        if is_well_defined:
            for g1, c1 in cosets:
                for g2, c2 in cosets:
                    if action(g1, x) == action(g2, x):
                        if not cosets_equal(c1, c2):
                            is_injective = False
                            break
                if not is_injective: break
                
        is_surjective = True
        if is_well_defined and is_injective:
            for y in X:
                can_reach = False
                for g in G:
                    if action(g, x) == y:
                        can_reach = True
                        break
                if not can_reach:
                    is_surjective = False
                    break
                    
        neg_q = not (is_well_defined and is_injective and is_surjective)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts transitively on X",
    "H_3: x in X",
    "H_4: H = Stab(x)",
    "not Q: The map phi(gH) = g.x is not a G-set isomorphism"
]

N_HYP = 4
NEG_Q_INDEX = 4