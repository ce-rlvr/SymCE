import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *

# Top-level setup for potential witness references
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            Y = witness.get('Y')
            action_X = witness.get('action_X')
            action_Y = witness.get('action_Y')
            f = witness.get('f')
            x_elem = witness.get('x')
        else:
            G = getattr(witness, 'G', None)
            X = getattr(witness, 'X', None)
            Y = getattr(witness, 'Y', None)
            action_X = getattr(witness, 'action_X', None)
            action_Y = getattr(witness, 'action_Y', None)
            f = getattr(witness, 'f', None)
            x_elem = getattr(witness, 'x', None)
            
        if G is None or X is None or Y is None or action_X is None or action_Y is None or f is None or x_elem is None:
            return [False] * 6
            
        X = list(X)
        Y = list(Y)
        
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
            
        if isinstance(action_X, dict):
            act_X = lambda g, x: action_X[(g, x)]
        else:
            act_X = action_X
            
        if isinstance(action_Y, dict):
            act_Y = lambda g, y: action_Y[(g, y)]
        else:
            act_Y = action_Y
            
    except Exception:
        return [False] * 6

    # H_1: G is a group acting on X
    try:
        h1 = True
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        if hasattr(G, 'identity'):
            identity = G.identity
        else:
            identity = None
            for e in elements:
                if e * e == e:
                    identity = e
                    break
                    
        if identity is None:
            h1 = False
            
        if h1:
            for item in X:
                if act_X(identity, item) != item:
                    h1 = False
                    break
                    
        if h1:
            for g in elements:
                for item in X:
                    if act_X(g, item) not in X:
                        h1 = False
                        break
                if not h1: break
                
        if h1:
            is_left = True
            is_right = True
            for g in elements:
                for h in elements:
                    gh = g * h
                    for item in X:
                        if is_left and act_X(gh, item) != act_X(g, act_X(h, item)):
                            is_left = False
                        if is_right and act_X(gh, item) != act_X(h, act_X(g, item)):
                            is_right = False
                    if not is_left and not is_right:
                        break
                if not is_left and not is_right:
                    break
            if not is_left and not is_right:
                h1 = False
    except Exception:
        h1 = False

    # H_2: G is a group acting on Y
    try:
        h2 = True
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        if hasattr(G, 'identity'):
            identity = G.identity
        else:
            identity = None
            for e in elements:
                if e * e == e:
                    identity = e
                    break
                    
        if identity is None:
            h2 = False
            
        if h2:
            for item in Y:
                if act_Y(identity, item) != item:
                    h2 = False
                    break
                    
        if h2:
            for g in elements:
                for item in Y:
                    if act_Y(g, item) not in Y:
                        h2 = False
                        break
                if not h2: break
                
        if h2:
            is_left = True
            is_right = True
            for g in elements:
                for h in elements:
                    gh = g * h
                    for item in Y:
                        if is_left and act_Y(gh, item) != act_Y(g, act_Y(h, item)):
                            is_left = False
                        if is_right and act_Y(gh, item) != act_Y(h, act_Y(g, item)):
                            is_right = False
                    if not is_left and not is_right:
                        break
                if not is_left and not is_right:
                    break
            if not is_left and not is_right:
                h2 = False
    except Exception:
        h2 = False

    # H_3: f maps X to Y
    try:
        h3 = True
        for item in X:
            if f_func(item) not in Y:
                h3 = False
                break
    except Exception:
        h3 = False

    # H_4: f is G-equivariant
    try:
        h4 = True
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        for g in elements:
            for item in X:
                if f_func(act_X(g, item)) != act_Y(g, f_func(item)):
                    h4 = False
                    break
            if not h4: break
    except Exception:
        h4 = False

    # H_5: x is an element of X
    try:
        h5 = x_elem in X
    except Exception:
        h5 = False

    # ¬Q: The stabilizer of x in G is NOT equal to the stabilizer of f(x) in G
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        stab_x = []
        for g in elements:
            if act_X(g, x_elem) == x_elem:
                stab_x.append(g)
                
        fx = f_func(x_elem)
        stab_fx = []
        for g in elements:
            if act_Y(g, fx) == fx:
                stab_fx.append(g)
                
        neg_q = False
        if len(stab_x) != len(stab_fx):
            neg_q = True
        else:
            for g in stab_x:
                if g not in stab_fx:
                    neg_q = True
                    break
            if not neg_q:
                for g in stab_fx:
                    if g not in stab_x:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on X",
    "H_2: G is a group acting on Y",
    "H_3: f maps X to Y",
    "H_4: f is G-equivariant",
    "H_5: x is an element of X",
    "¬Q: The stabilizer of x in G is NOT equal to the stabilizer of f(x) in G"
]

N_HYP = 5
NEG_Q_INDEX = 5