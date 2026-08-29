import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Orbit-Stabilizer Theorem.
    Witness is expected to be a tuple: (G, X, action, x)
    where:
      - G is a SymPy PermutationGroup (or similar object with .elements, .order(), .identity)
      - X is an iterable representing the set
      - action is a callable action(g, y) or a dict mapping (g, y) to an element in X
      - x is an element in X
    """
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, X, action, x = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'order') and hasattr(G, 'identity')
        if h1:
            order = G.order()
            if order == float('inf'):
                h1 = False
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.elements)
            e = G.identity
            X_list = list(X)
            
            if isinstance(action, dict):
                act = lambda g, y: action[(g, y)]
            else:
                act = action
                
            is_closed = True
            for g in elements:
                for y in X_list:
                    if act(g, y) not in X_list:
                        is_closed = False
                        break
                if not is_closed:
                    break
                    
            if not is_closed:
                h2 = False
            else:
                h2_identity = True
                for y in X_list:
                    if act(e, y) != y:
                        h2_identity = False
                        break
                
                if not h2_identity:
                    h2 = False
                else:
                    is_left = True
                    is_right = True
                    for g in elements:
                        for h in elements:
                            gh = g * h
                            for y in X_list:
                                res_gh = act(gh, y)
                                if res_gh != act(g, act(h, y)):
                                    is_left = False
                                if res_gh != act(h, act(g, y)):
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

    # H3: x \in X
    try:
        X_list = list(X)
        h3 = x in X_list
    except Exception:
        h3 = False

    # neg_Q: |G| != |Orb(x)| * |Stab(x)|
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(G.elements)
            
            if isinstance(action, dict):
                act = lambda g, y: action[(g, y)]
            else:
                act = action
                
            orb = []
            for g in elements:
                res = act(g, x)
                if res not in orb:
                    orb.append(res)
            
            stab_count = 0
            for g in elements:
                if act(g, x) == x:
                    stab_count += 1
                    
            order = G.order()
            
            neg_q = order != len(orb) * stab_count
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G acts on X",
    "H_3: x \\in X",
    "¬Q: |G| != |Orb(x)| \\cdot |Stab(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3