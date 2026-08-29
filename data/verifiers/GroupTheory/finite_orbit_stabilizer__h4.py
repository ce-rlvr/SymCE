import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def safe_eq(a, b):
    """Safely check equality, handling sympy symbolic equality objects."""
    if a is b:
        return True
    try:
        res = (a == b)
        if isinstance(res, bool):
            return res
    except Exception:
        pass
    try:
        if hasattr(a, 'equals'):
            return bool(a.equals(b))
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    Witness is expected to provide: G (group), X (set), action (callable or dict), x (element).
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            action = witness['action']
            x = witness['x']
        else:
            G, X, action, x = witness
    except Exception:
        return [False, False, False, False]

    if isinstance(action, dict):
        def act(g, y):
            return action[(g, y)]
    else:
        act = action

    # H1: G is a finite group
    try:
        if hasattr(G, 'order'):
            order = G.order()
        else:
            order = len(G)
        h1 = bool(order > 0 and order != sympy.oo)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        _ = len(X)
        for _item in X:
            break
        h2 = True
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        if hasattr(G, 'identity'):
            e = G.identity
        else:
            e = elements[0]
            
        h3_id = True
        for y in X:
            try:
                if not safe_eq(act(e, y), y):
                    h3_id = False
                    break
            except Exception:
                h3_id = False
                break
                
        if not h3_id:
            h3 = False
        else:
            is_left = True
            is_right = True
            for g in elements:
                for h in elements:
                    try:
                        gh = g * h
                    except Exception:
                        is_left = False
                        is_right = False
                        break
                        
                    for y in X:
                        if is_left:
                            try:
                                if not safe_eq(act(gh, y), act(g, act(h, y))):
                                    is_left = False
                            except Exception:
                                is_left = False
                        if is_right:
                            try:
                                if not safe_eq(act(gh, y), act(h, act(g, y))):
                                    is_right = False
                            except Exception:
                                is_right = False
                        if not is_left and not is_right:
                            break
                    if not is_left and not is_right:
                        break
                if not is_left and not is_right:
                    break
            h3 = bool(is_left or is_right)
    except Exception:
        h3 = False

    # neg_Q: |G| != |Orb_G(x)| * |Stab_G(x)|
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        orb = []
        stab_count = 0
        for g in elements:
            res = act(g, x)
            found = False
            for item in orb:
                if safe_eq(item, res):
                    found = True
                    break
            if not found:
                orb.append(res)
                
            if safe_eq(res, x):
                stab_count += 1
                
        neg_q = bool(len(elements) != len(orb) * stab_count)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "¬Q: |G| != |Orb_G(x)| * |Stab_G(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3