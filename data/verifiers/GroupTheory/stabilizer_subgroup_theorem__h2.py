import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
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

def get_group_info(G):
    if hasattr(G, 'generate') and hasattr(G, 'identity'):
        elements = list(G.generate())
        identity = G.identity
        op = lambda a, b: a * b
        inv = lambda a: a**-1
        return elements, identity, op, inv
    elif hasattr(G, 'elements') and hasattr(G, 'identity'):
        elements = list(G.elements)
        identity = G.identity
        op = lambda a, b: a * b
        inv = lambda a: a**-1
        return elements, identity, op, inv
    elif isinstance(G, tuple) and len(G) == 4:
        return G
    elif isinstance(G, dict):
        return G['elements'], G['identity'], G['op'], G['inv']
    return None

def check_group(G):
    info = get_group_info(G)
    if not info: 
        return False
    elements, identity, op, inv = info
    
    if not elements: 
        return False
    if identity not in elements: 
        return False
    
    # Check closure
    for a in elements:
        for b in elements:
            try:
                if op(a, b) not in elements: 
                    return False
            except Exception:
                return False
                
    # Check identity
    for a in elements:
        try:
            if op(identity, a) != a or op(a, identity) != a: 
                return False
        except Exception:
            return False
            
    # Check inverses
    for a in elements:
        try:
            if op(a, inv(a)) != identity or op(inv(a), a) != identity: 
                return False
        except Exception:
            return False
            
    # Check associativity
    for a in elements:
        for b in elements:
            for c in elements:
                try:
                    if op(op(a, b), c) != op(a, op(b, c)): 
                        return False
                except Exception:
                    return False
                    
    return True

def check_action(G, X, action):
    info = get_group_info(G)
    if not info: 
        return False
    elements, _, _, _ = info
    
    if not isinstance(X, (set, list, tuple)): 
        return False
    X_list = list(X)
    
    for g in elements:
        for y in X_list:
            try:
                res = action(g, y)
                if res not in X_list: 
                    return False
            except Exception:
                return False
    return True

def check_x_in_X(X, x):
    if not isinstance(X, (set, list, tuple)): 
        return False
    return x in list(X)

def check_neg_Q(G, action, x):
    info = get_group_info(G)
    if not info: 
        return False
    elements, identity, op, inv = info
    
    stab = []
    for g in elements:
        try:
            if action(g, x) == x:
                stab.append(g)
        except Exception:
            pass
            
    # A subgroup must contain the identity
    if identity not in stab:
        return True
        
    # A subgroup must be closed under the group operation
    for a in stab:
        for b in stab:
            try:
                if op(a, b) not in stab:
                    return True
            except Exception:
                return True
                
    # A subgroup must be closed under inverses
    for a in stab:
        try:
            if inv(a) not in stab:
                return True
        except Exception:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            action = witness.get('action')
            x = witness.get('x')
        else:
            G, X, action, x = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_group(G)
    except Exception:
        h1 = False
        
    try:
        h2 = check_action(G, X, action)
    except Exception:
        h2 = False
        
    try:
        h3 = check_x_in_X(X, x)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(G, action, x)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "H_3: x in X",
    "¬Q: Stab(x) is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3