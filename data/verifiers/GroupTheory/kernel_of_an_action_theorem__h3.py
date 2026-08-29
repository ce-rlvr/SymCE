import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def get_group_elements_and_op(G_obj, op_obj):
    if hasattr(G_obj, 'elements') and hasattr(G_obj, 'is_group'):
        return list(G_obj.elements), lambda a, b: a * b
    return list(G_obj), op_obj

def is_group(G, op):
    try:
        G = list(G)
        if not G: return False
        # closure
        for a in G:
            for b in G:
                if op(a, b) not in G: return False
        # associativity
        for a in G:
            for b in G:
                for c in G:
                    if op(op(a, b), c) != op(a, op(b, c)): return False
        # identity
        id_elem = None
        for e in G:
            if all(op(e, a) == a and op(a, e) == a for a in G):
                id_elem = e
                break
        if id_elem is None: return False
        # inverses
        for a in G:
            has_inv = False
            for b in G:
                if op(a, b) == id_elem and op(b, a) == id_elem:
                    has_inv = True
                    break
            if not has_inv: return False
        return True
    except Exception:
        return False

def get_id_and_inv(G, op):
    G = list(G)
    id_elem = None
    for e in G:
        if all(op(e, a) == a and op(a, e) == a for a in G):
            id_elem = e
            break
    def inv(g):
        for b in G:
            if op(g, b) == id_elem and op(b, g) == id_elem:
                return b
        return None
    return id_elem, inv

def unique_elements(lst):
    res = []
    for e in lst:
        if not any(e == r for r in res):
            res.append(e)
    return res

def is_in(elem, lst):
    return any(elem == e for e in lst)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G_obj = witness.get('G')
            op_obj = witness.get('op')
            X_obj = witness.get('X')
            action = witness.get('action')
            K_obj = witness.get('K')
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                G_obj, op_obj, X_obj, action, K_obj = witness
            elif len(witness) == 4:
                G_obj, X_obj, action, K_obj = witness
                op_obj = None
            else:
                return [False, False, False]
        else:
            G_obj = getattr(witness, 'G', None)
            op_obj = getattr(witness, 'op', None)
            X_obj = getattr(witness, 'X', None)
            action = getattr(witness, 'action', None)
            K_obj = getattr(witness, 'K', None)

        G, op = get_group_elements_and_op(G_obj, op_obj)
        
        if hasattr(X_obj, 'elements'):
            X = list(X_obj.elements)
        else:
            X = list(X_obj)
            
        if hasattr(K_obj, 'elements'):
            K = list(K_obj.elements)
        else:
            K = list(K_obj)
    except Exception:
        return [False, False, False]

    # H1: G is a group acting on a set X
    h1_ok = False
    try:
        if is_group(G, op):
            h1_ok = True
            for g in G:
                for x in X:
                    if not is_in(action(g, x), X):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H2: K = {g \in G | g \cdot x = x for all x \in X}
    h2_ok = False
    try:
        expected_K = []
        for g in G:
            if all(action(g, x) == x for x in X):
                expected_K.append(g)
        
        K_u = unique_elements(K)
        expected_K_u = unique_elements(expected_K)
        
        if len(K_u) == len(expected_K_u) and all(is_in(k, expected_K_u) for k in K_u):
            h2_ok = True
    except Exception:
        h2_ok = False

    # Conclusion: K is a normal subgroup of G and is equal to the intersection \bigcap_{x \in X} G_x
    neg_q = False
    try:
        id_elem, inv_func = get_id_and_inv(G, op)
        K_u = unique_elements(K)
        
        is_normal_subgroup = True
        if not K_u:
            is_normal_subgroup = False
        else:
            if not is_in(id_elem, K_u):
                is_normal_subgroup = False
            
            # closure
            if is_normal_subgroup:
                for k1 in K_u:
                    for k2 in K_u:
                        if not is_in(op(k1, k2), K_u):
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
            
            # inverses
            if is_normal_subgroup:
                for k in K_u:
                    k_inv = inv_func(k)
                    if not is_in(k_inv, K_u):
                        is_normal_subgroup = False
                        break
            
            # normality
            if is_normal_subgroup:
                for g in G:
                    g_inv = inv_func(g)
                    for k in K_u:
                        conj = op(g, op(k, g_inv))
                        if not is_in(conj, K_u):
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break

        # Intersection
        if not X:
            intersection_Gx = unique_elements(G)
        else:
            intersection_Gx = unique_elements(G)
            for x in X:
                Gx = [g for g in G if action(g, x) == x]
                intersection_Gx = [g for g in intersection_Gx if is_in(g, Gx)]
        
        is_equal_to_intersection = (len(K_u) == len(intersection_Gx) and 
                                    all(is_in(k, intersection_Gx) for k in K_u))
        
        conclusion = is_normal_subgroup and is_equal_to_intersection
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: K is the kernel of the action",
    "¬Q: K is not a normal subgroup of G or is not equal to the intersection of stabilizers"
]

N_HYP = 2
NEG_Q_INDEX = 2