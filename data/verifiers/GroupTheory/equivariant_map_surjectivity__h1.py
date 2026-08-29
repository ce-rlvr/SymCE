import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_elements_and_id(G):
    elements = list(G.elements) if hasattr(G, 'elements') else list(G)
    if hasattr(G, 'identity'):
        id_g = G.identity
    else:
        id_g = None
        for e in elements:
            is_id = True
            for g in elements:
                try:
                    if e * g != g or g * e != g:
                        is_id = False
                        break
                except Exception:
                    is_id = False
                    break
            if is_id:
                id_g = e
                break
    return elements, id_g

def check_H1(witness):
    try:
        G = witness['G']
        Y = list(witness['Y'])
        action_Y = witness['action_Y']
        
        if not Y:
            return False
            
        elements, id_g = get_elements_and_id(G)
        if not elements:
            return False
            
        # Check closure
        for g in elements:
            for y in Y:
                if action_Y(g, y) not in Y:
                    return False
                    
        # Check identity
        if id_g is not None:
            for y in Y:
                if action_Y(id_g, y) != y:
                    return False
                    
        # Check action property (left or right action)
        is_left = True
        is_right = True
        for g1 in elements:
            for g2 in elements:
                g1g2 = g1 * g2
                for y in Y:
                    res = action_Y(g1g2, y)
                    if is_left and res != action_Y(g1, action_Y(g2, y)):
                        is_left = False
                    if is_right and res != action_Y(g2, action_Y(g1, y)):
                        is_right = False
        if not (is_left or is_right):
            return False
            
        # Check transitivity
        y0 = Y[0]
        orbit = []
        for g in elements:
            gy = action_Y(g, y0)
            if gy not in orbit:
                orbit.append(gy)
                
        for y in Y:
            if y not in orbit:
                return False
                
        return True
    except Exception:
        return False

def check_H2(witness):
    try:
        G = witness['G']
        X = list(witness['X'])
        Y = list(witness['Y'])
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        phi = witness['phi']
        
        elements, id_g = get_elements_and_id(G)
        if not elements:
            return False
            
        if X:
            # Check closure of action_X
            for g in elements:
                for x in X:
                    if action_X(g, x) not in X:
                        return False
                        
            # Check identity on X
            if id_g is not None:
                for x in X:
                    if action_X(id_g, x) != x:
                        return False
            
            # Check action property on X
            is_left = True
            is_right = True
            for g1 in elements:
                for g2 in elements:
                    g1g2 = g1 * g2
                    for x in X:
                        res = action_X(g1g2, x)
                        if is_left and res != action_X(g1, action_X(g2, x)):
                            is_left = False
                        if is_right and res != action_X(g2, action_X(g1, x)):
                            is_right = False
            if not (is_left or is_right):
                return False
                
        # Check equivariance
        for x in X:
            px = phi(x)
            if px not in Y:
                return False
            for g in elements:
                if phi(action_X(g, x)) != action_Y(g, px):
                    return False
                    
        return True
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        X = list(witness['X'])
        Y = list(witness['Y'])
        phi = witness['phi']
        
        image = []
        for x in X:
            px = phi(x)
            if px not in image:
                image.append(px)
                
        # Check if phi is NOT surjective
        for y in Y:
            if y not in image:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: G acts transitively on a non-empty set Y",
    "H_2: phi: X -> Y is a G-equivariant map",
    "¬Q: The map phi is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2