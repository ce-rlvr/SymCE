import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def extract(witness):
    if isinstance(witness, dict):
        X = witness.get('X')
        G = witness.get('G')
        action = witness.get('action')
        op = witness.get('op')
        x = witness.get('x')
        g = witness.get('g')
        y = witness.get('y')
        return X, G, action, op, x, g, y
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 5:
            return witness[0], witness[1], None, None, witness[2], witness[3], witness[4]
        elif len(witness) == 6:
            return witness[0], witness[1], witness[2], None, witness[3], witness[4], witness[5]
        elif len(witness) == 7:
            return witness[0], witness[1], witness[2], witness[3], witness[4], witness[5], witness[6]
    raise ValueError("Unknown witness format")

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return list(obj.elements)
    if hasattr(obj, 'generate'):
        return list(obj.generate())
    if isinstance(obj, (list, set, tuple)):
        return list(obj)
    raise ValueError("Cannot get elements")

def apply_action(h, x, action=None):
    if action is not None:
        if isinstance(action, dict):
            return action[(h, x)]
        return action(h, x)
    try:
        return h(x)
    except Exception:
        pass
    try:
        return h * x
    except Exception:
        pass
    raise ValueError("Cannot apply action")

def apply_op(h1, h2, op=None):
    if op is not None:
        if isinstance(op, dict):
            return op[(h1, h2)]
        return op(h1, h2)
    try:
        return h1 * h2
    except Exception:
        pass
    try:
        return h1(h2)
    except Exception:
        pass
    raise ValueError("Cannot apply op")

def find_identity(G_elems, op=None):
    for e in G_elems:
        is_id = True
        for h in G_elems:
            if apply_op(e, h, op) != h or apply_op(h, e, op) != h:
                is_id = False
                break
        if is_id:
            return e
    return None

def conditions(witness) -> list[bool]:
    try:
        X, G, action, op, x, g, y = extract(witness)
    except Exception:
        return [False, False, False, False, False, False]
        
    # H1: X is a set
    try:
        X_elems = get_elements(X)
        h1 = True
    except Exception:
        h1 = False
        
    # H2: G acts on X
    try:
        G_elems = get_elements(G)
        id_elem = find_identity(G_elems, op)
        if id_elem is None:
            h2 = False
        else:
            h2 = True
            for g1 in G_elems:
                for g2 in G_elems:
                    g12 = apply_op(g1, g2, op)
                    if g12 not in G_elems:
                        h2 = False; break
                    for g3 in G_elems:
                        if apply_op(g1, apply_op(g2, g3, op), op) != apply_op(g12, g3, op):
                            h2 = False; break
                    if not h2: break
                if not h2: break
                
            if h2:
                for x_elem in X_elems:
                    if apply_action(id_elem, x_elem, action) != x_elem:
                        h2 = False; break
                    for g1 in G_elems:
                        g1x = apply_action(g1, x_elem, action)
                        if g1x not in X_elems:
                            h2 = False; break
                        for g2 in G_elems:
                            g12 = apply_op(g1, g2, op)
                            if apply_action(g12, x_elem, action) != apply_action(g1, apply_action(g2, x_elem, action), action):
                                h2 = False; break
                        if not h2: break
                    if not h2: break
    except Exception:
        h2 = False
        
    # H3: x \in X
    try:
        h3 = x in X_elems
    except Exception:
        h3 = False
        
    # H4: g \in G
    try:
        h4 = g in G_elems
    except Exception:
        h4 = False
        
    # H5: y = g \cdot x
    try:
        h5 = y == apply_action(g, x, action)
    except Exception:
        h5 = False
        
    # Q: Stab(y) = g Stab(x) g^{-1}
    try:
        stab_x = [h for h in G_elems if apply_action(h, x, action) == x]
        stab_y = [h for h in G_elems if apply_action(h, y, action) == y]
        
        id_elem = find_identity(G_elems, op)
        
        g_inv = None
        for inv in G_elems:
            if apply_op(g, inv, op) == id_elem and apply_op(inv, g, op) == id_elem:
                g_inv = inv
                break
                
        if g_inv is None:
            q_ok = False
        else:
            rhs = []
            for h in stab_x:
                gh = apply_op(g, h, op)
                ghg = apply_op(gh, g_inv, op)
                rhs.append(ghg)
                
            q_ok = True
            for elem in stab_y:
                if elem not in rhs:
                    q_ok = False; break
            if q_ok:
                for elem in rhs:
                    if elem not in stab_y:
                        q_ok = False; break
    except Exception:
        q_ok = False
        
    neg_q = not q_ok
    
    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: x in X",
    "H_4: g in G",
    "H_5: y = g \\cdot x",
    "¬Q: Stab(y) != g Stab(x) g^{-1}"
]

N_HYP = 5
NEG_Q_INDEX = 5