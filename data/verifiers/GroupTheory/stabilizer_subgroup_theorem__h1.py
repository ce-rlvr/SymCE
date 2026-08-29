import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    if isinstance(witness, dict):
        G = witness.get('G', [])
        op = witness.get('op', None)
        X = witness.get('X', [])
        action = witness.get('action', None)
        x = witness.get('x', None)
    else:
        G = getattr(witness, 'G', [])
        op = getattr(witness, 'op', None)
        X = getattr(witness, 'X', [])
        action = getattr(witness, 'action', None)
        x = getattr(witness, 'x', None)

    def _op(g, h):
        if callable(op):
            return op(g, h)
        return op[(g, h)]

    def _action(g, y):
        if callable(action):
            return action(g, y)
        return action[(g, y)]

    # H1: X is a set
    try:
        h1 = isinstance(X, (list, set, tuple, frozenset))
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        h2 = False
        if isinstance(G, (list, set, tuple, frozenset)) and (callable(op) or isinstance(op, dict)) and (callable(action) or isinstance(action, dict)):
            G_list = list(G)
            X_list = list(X)
            
            if len(G_list) > 0 and len(X_list) > 0:
                closed_op = True
                for g in G_list:
                    for h in G_list:
                        if _op(g, h) not in G_list:
                            closed_op = False
                            break
                    if not closed_op: break
                
                if closed_op:
                    closed_act = True
                    for g in G_list:
                        for y in X_list:
                            if _action(g, y) not in X_list:
                                closed_act = False
                                break
                        if not closed_act: break
                    
                    if closed_act:
                        assoc_op = True
                        for g in G_list:
                            for h in G_list:
                                for k in G_list:
                                    if _op(_op(g, h), k) != _op(g, _op(h, k)):
                                        assoc_op = False
                                        break
                                if not assoc_op: break
                            if not assoc_op: break
                        
                        if assoc_op:
                            compat_act = True
                            for g in G_list:
                                for h in G_list:
                                    for y in X_list:
                                        if _action(_op(g, h), y) != _action(g, _action(h, y)):
                                            compat_act = False
                                            break
                                    if not compat_act: break
                                if not compat_act: break
                            
                            if compat_act:
                                has_id = False
                                for e in G_list:
                                    is_id = True
                                    for g in G_list:
                                        if _op(e, g) != g or _op(g, e) != g:
                                            is_id = False
                                            break
                                    if is_id:
                                        act_id = True
                                        for y in X_list:
                                            if _action(e, y) != y:
                                                act_id = False
                                                break
                                        if act_id:
                                            has_id = True
                                            break
                                
                                h2 = has_id
    except Exception:
        h2 = False

    # H3: x \in X
    try:
        h3 = False
        if isinstance(X, (list, set, tuple, frozenset)):
            h3 = x in list(X)
    except Exception:
        h3 = False

    # neg_Q: Stab(x) is NOT a subgroup of G
    try:
        neg_q = False
        if isinstance(G, (list, set, tuple, frozenset)) and (callable(op) or isinstance(op, dict)) and (callable(action) or isinstance(action, dict)):
            G_list = list(G)
            stab = [g for g in G_list if _action(g, x) == x]
            
            is_subgroup = True
            if not stab:
                is_subgroup = False
            else:
                for g in stab:
                    for h in stab:
                        if _op(g, h) not in stab:
                            is_subgroup = False
                            break
                    if not is_subgroup: break
                
                if is_subgroup:
                    id_stab = None
                    for e in stab:
                        is_e = True
                        for g in stab:
                            if _op(e, g) != g or _op(g, e) != g:
                                is_e = False
                                break
                        if is_e:
                            id_stab = e
                            break
                    
                    if id_stab is None:
                        is_subgroup = False
                    else:
                        for g in stab:
                            has_inv = False
                            for h in stab:
                                if _op(g, h) == id_stab and _op(h, g) == id_stab:
                                    has_inv = True
                                    break
                            if not has_inv:
                                is_subgroup = False
                                break
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: x in X",
    "¬Q: Stab(x) is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3