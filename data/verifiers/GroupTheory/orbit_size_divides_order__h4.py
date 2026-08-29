import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(G):
    if hasattr(G, 'order'):
        if callable(G.order):
            return G.order()
        return G.order
    if hasattr(G, '__len__'):
        return len(G)
    raise ValueError("Cannot determine order of G")

def get_elements(G):
    if hasattr(G, 'elements'):
        try:
            elts = list(G.elements)
            if len(elts) > 0:
                return elts
        except Exception:
            pass
    if hasattr(G, 'generate') and callable(G.generate):
        return list(G.generate())
    if hasattr(G, '__iter__'):
        return list(G)
    raise ValueError("Cannot get elements of G")

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    if hasattr(G, 'identity_element'):
        return G.identity_element
    elements = get_elements(G)
    for e in elements:
        is_id = True
        for x in elements:
            if e * x != x or x * e != x:
                is_id = False
                break
        if is_id:
            return e
    raise ValueError("Cannot find identity")

def is_finite_group(G):
    from sympy.combinatorics import PermutationGroup
    if isinstance(G, PermutationGroup):
        return True
    order = get_order(G)
    if order == float('inf') or order == sympy.oo:
        return False
    elements = get_elements(G)
    if len(elements) != order:
        return False
    e = get_identity(G)
    for g in elements:
        has_inv = False
        for h in elements:
            if g * h == e and h * g == e:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def is_set(X):
    if isinstance(X, (set, frozenset, list, tuple)):
        return True
    if hasattr(X, '__iter__') and hasattr(X, '__contains__'):
        return True
    return False

def apply_act(act, g, y):
    if callable(act):
        return act(g, y)
    elif isinstance(act, dict):
        return act[(g, y)]
    else:
        raise ValueError("act must be callable or dict")

def acts_on(G, X, act):
    elements = get_elements(G)
    e = get_identity(G)
    
    X_list = list(X)
    
    for y in X_list:
        if apply_act(act, e, y) != y:
            return False
        for g in elements:
            if apply_act(act, g, y) not in X_list:
                return False
            
    left_ok = True
    right_ok = True
    for g in elements:
        for h in elements:
            for y in X_list:
                if left_ok and apply_act(act, g * h, y) != apply_act(act, g, apply_act(act, h, y)):
                    left_ok = False
                if right_ok and apply_act(act, g * h, y) != apply_act(act, h, apply_act(act, g, y)):
                    right_ok = False
                if not left_ok and not right_ok:
                    return False
    return True

def check_acts_on(G, X, act):
    try:
        return acts_on(G, X, act)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            act = witness.get('act', witness.get('action'))
            x = witness['x']
        elif isinstance(witness, tuple) and len(witness) == 4:
            G, X, act, x = witness
        else:
            G = witness.G
            X = witness.X
            act = getattr(witness, 'act', getattr(witness, 'action', None))
            x = witness.x
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_finite_group(G)
    except Exception:
        h1 = False

    try:
        h2 = is_set(X)
    except Exception:
        h2 = False

    try:
        h3 = check_acts_on(G, X, act)
    except Exception:
        h3 = False

    try:
        elements = get_elements(G)
        orbit = []
        for g in elements:
            res = apply_act(act, g, x)
            if res not in orbit:
                orbit.append(res)
        orbit_size = len(orbit)
        order = get_order(G)
        neg_q = (order % orbit_size != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "¬Q: The cardinality of the orbit of x does not divide the order of the group |G|"
]

N_HYP = 3
NEG_Q_INDEX = 3