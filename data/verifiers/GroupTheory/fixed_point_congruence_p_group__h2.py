import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    """
    witness is expected to be a dict with keys:
      'P': group (e.g., a sympy PermutationGroup or a list of elements closed under '*')
      'X': list or set of elements
      'action': callable action(g, x)
      'p': integer
      'X_P': (optional) list of fixed points
    """
    
    # H1: P is a finite p-group
    h1 = False
    try:
        P = witness['P']
        p = witness['p']
        elements = list(P.elements) if hasattr(P, 'elements') else list(P)
        order = len(elements)
        if p > 1 and order > 0:
            # check closure
            closed = True
            for g in elements:
                for h in elements:
                    if (g * h) not in elements:
                        closed = False
                        break
                if not closed: break
            
            if closed:
                temp = order
                while temp % p == 0:
                    temp //= p
                if temp == 1:
                    h1 = True
    except Exception:
        h1 = False

    # H2: P acts on X
    h2 = False
    try:
        P = witness['P']
        elements = list(P.elements) if hasattr(P, 'elements') else list(P)
        X = witness['X']
        action = witness['action']
        
        # find identity
        identity = None
        for g in elements:
            if all(g * h == h for h in elements):
                identity = g
                break
                
        if identity is not None:
            # check axiom 1
            ax1 = all(action(identity, x) == x for x in X)
            
            # check axiom 2 (left action)
            ax2_left = True
            for g in elements:
                for h in elements:
                    gh = g * h
                    for x in X:
                        if action(g, action(h, x)) != action(gh, x):
                            ax2_left = False
                            break
                    if not ax2_left: break
                if not ax2_left: break
                
            # check axiom 2 (right action)
            ax2_right = True
            for g in elements:
                for h in elements:
                    gh = g * h
                    for x in X:
                        if action(h, action(g, x)) != action(gh, x):
                            ax2_right = False
                            break
                    if not ax2_right: break
                if not ax2_right: break
                
            if ax1 and (ax2_left or ax2_right):
                h2 = True
    except Exception:
        h2 = False

    # H3: X^P is the set of elements in X fixed by all elements of P
    h3 = False
    try:
        P = witness['P']
        elements = list(P.elements) if hasattr(P, 'elements') else list(P)
        X = witness['X']
        action = witness['action']
        
        actual_X_P = []
        for x in X:
            if all(action(g, x) == x for g in elements):
                actual_X_P.append(x)
        
        if 'X_P' in witness:
            X_P = witness['X_P']
            matched = []
            h3 = True
            if len(X_P) != len(actual_X_P):
                h3 = False
            else:
                for x in X_P:
                    found = False
                    for i, ax in enumerate(actual_X_P):
                        if i not in matched and x == ax:
                            matched.append(i)
                            found = True
                            break
                    if not found:
                        h3 = False
                        break
        else:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: |X| \equiv |X^P| \pmod p is FALSE
    neg_q = False
    try:
        X = witness['X']
        p = witness['p']
        if 'X_P' in witness:
            X_P = witness['X_P']
        else:
            P = witness['P']
            elements = list(P.elements) if hasattr(P, 'elements') else list(P)
            action = witness['action']
            X_P = [x for x in X if all(action(g, x) == x for g in elements)]
            
        len_X = len(X)
        len_X_P = len(X_P)
        if len_X % p != len_X_P % p:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a finite p-group",
    "H_2: P acts on X",
    "H_3: X^P is the set of elements in X fixed by all elements of P",
    "¬Q: |X| is not congruent to |X^P| modulo p"
]

N_HYP = 3
NEG_Q_INDEX = 3