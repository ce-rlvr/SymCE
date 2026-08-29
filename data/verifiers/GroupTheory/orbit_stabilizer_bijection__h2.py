import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G_elements = witness['G_elements']
            op = witness['op']
            X_elements = witness['X_elements']
            action = witness['action']
            x = witness['x']
        else:
            G_elements, op, X_elements, action, x = witness
            
        G_elements = list(G_elements)
        X_elements = list(X_elements)
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        if not G_elements:
            h1 = False
        else:
            closure = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if op(g1, g2) not in G_elements:
                        closure = False
                        break
                if not closure: break
            
            if not closure:
                h1 = False
            else:
                assoc = True
                for g1 in G_elements:
                    for g2 in G_elements:
                        for g3 in G_elements:
                            if op(g1, op(g2, g3)) != op(op(g1, g2), g3):
                                assoc = False
                                break
                        if not assoc: break
                    if not assoc: break
                
                if not assoc:
                    h1 = False
                else:
                    identity = None
                    for e in G_elements:
                        is_id = True
                        for g in G_elements:
                            if op(e, g) != g or op(g, e) != g:
                                is_id = False
                                break
                        if is_id:
                            identity = e
                            break
                    
                    if identity is None:
                        h1 = False
                    else:
                        inv_ok = True
                        for g in G_elements:
                            has_inv = False
                            for h in G_elements:
                                if op(g, h) == identity and op(h, g) == identity:
                                    has_inv = True
                                    break
                            if not has_inv:
                                inv_ok = False
                                break
                        h1 = inv_ok
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        if not X_elements:
            h2 = False
        else:
            closure_act = True
            for g in G_elements:
                for y in X_elements:
                    if action(g, y) not in X_elements:
                        closure_act = False
                        break
                if not closure_act: break
            
            if not closure_act:
                h2 = False
            else:
                identities = [e for e in G_elements if all(op(e, g) == g and op(g, e) == g for g in G_elements)]
                if not identities:
                    h2 = False
                else:
                    e = identities[0]
                    id_acts_trivially = all(action(e, y) == y for y in X_elements)
                    if not id_acts_trivially:
                        h2 = False
                    else:
                        is_left = True
                        is_right = True
                        for g1 in G_elements:
                            for g2 in G_elements:
                                for y in X_elements:
                                    if action(op(g1, g2), y) != action(g1, action(g2, y)):
                                        is_left = False
                                    if action(op(g1, g2), y) != action(g2, action(g1, y)):
                                        is_right = False
                                    if not is_left and not is_right:
                                        break
                                if not is_left and not is_right:
                                    break
                            if not is_left and not is_right:
                                break
                        h2 = is_left or is_right
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X_elements
    except Exception:
        h3 = False

    # neg_Q: The map g*Stab_G(x) |-> g.x is NOT a bijection
    try:
        identities = [e for e in G_elements if all(op(e, g) == g and op(g, e) == g for g in G_elements)]
        if not identities:
            neg_q = False
        else:
            stab_x = [g for g in G_elements if action(g, x) == x]
            
            def coset_eq(c1, c2):
                s1 = []
                for elem in c1:
                    if elem not in s1: s1.append(elem)
                s2 = []
                for elem in c2:
                    if elem not in s2: s2.append(elem)
                if len(s1) != len(s2): return False
                for elem in s1:
                    if elem not in s2: return False
                return True
            
            left_cosets = []
            for g in G_elements:
                coset = [op(g, s) for s in stab_x]
                left_cosets.append((g, coset))
            
            is_well_defined = True
            is_injective = True
            
            for g1, c1 in left_cosets:
                for g2, c2 in left_cosets:
                    same_coset = coset_eq(c1, c2)
                    same_action = (action(g1, x) == action(g2, x))
                    
                    if same_coset and not same_action:
                        is_well_defined = False
                    if same_action and not same_coset:
                        is_injective = False
                        
            neg_q = not (is_well_defined and is_injective)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: The map g*Stab_G(x) |-> g.x is not a bijection"
]

N_HYP = 3
NEG_Q_INDEX = 3