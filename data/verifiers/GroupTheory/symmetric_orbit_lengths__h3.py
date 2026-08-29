import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a finite set on which G acts transitively",
    "H_3: G_x and G_y are the stabilizers of x and y in G, respectively",
    "¬Q: The cardinality of the orbit of y under G_x is not equal to the cardinality of the orbit of x under G_y"
]

N_HYP = 3
NEG_Q_INDEX = 3

def apply_action(g, p, action=None):
    if action is not None:
        return action(g, p)
    if hasattr(g, '__call__'):
        try:
            return g(p)
        except Exception:
            pass
    if hasattr(g, '^'):
        try:
            return g ^ p
        except Exception:
            pass
    try:
        return g * p
    except Exception:
        pass
    raise ValueError("No action defined")

def is_group(G):
    if hasattr(G, 'is_group') and G.is_group:
        return True
    if hasattr(G, 'elements') or hasattr(G, 'generators'):
        return True
    if isinstance(G, PermutationGroup):
        return True
    return False

def is_finite_transitive_action(G, X, action):
    try:
        if not isinstance(X, (list, set, tuple)):
            return False
        if len(X) == 0 or len(X) > 1000:
            return False
            
        if isinstance(G, PermutationGroup) and action is None:
            try:
                if set(X) == set(range(G.degree)):
                    return G.is_transitive()
                x0 = list(X)[0]
                if x0 >= G.degree:
                    return set(X) == {x0}
                orbit = set(G.orbit(x0))
                return orbit == set(X)
            except TypeError:
                pass
                
        x0 = list(X)[0]
        orbit = [x0]
        queue = [x0]
        gens = G.generators if hasattr(G, 'generators') else G.elements
        while queue:
            if len(orbit) > len(X):
                return False
            curr = queue.pop(0)
            for g in gens:
                nxt = apply_action(g, curr, action)
                if nxt not in orbit:
                    orbit.append(nxt)
                    queue.append(nxt)
        
        if len(orbit) != len(X):
            return False
        for o in orbit:
            if o not in X:
                return False
        return True
    except Exception:
        return False

def get_stabilizer(G, pt, action=None):
    if isinstance(G, PermutationGroup) and action is None:
        if pt < G.degree:
            return G.stabilizer(pt)
        else:
            return G
    else:
        if hasattr(G, 'elements'):
            class DummyGroup:
                def __init__(self, elems):
                    self.elements = elems
                    self.generators = elems
            elems = []
            for i, g in enumerate(G.elements):
                if i > 10000:
                    break
                if apply_action(g, pt, action) == pt:
                    elems.append(g)
            return DummyGroup(elems)
        return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            x = witness.get('x')
            y = witness.get('y')
            G_x = witness.get('G_x')
            G_y = witness.get('G_y')
            action = witness.get('action')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, x, y = witness
                X = G_x = G_y = action = None
            elif len(witness) == 4:
                G, X, x, y = witness
                G_x = G_y = action = None
            elif len(witness) == 5:
                G, X, x, y, action = witness
                G_x = G_y = None
            elif len(witness) >= 6:
                G = witness[0]
                X = witness[1]
                x = witness[2]
                y = witness[3]
                G_x = witness[4]
                G_y = witness[5]
                action = witness[6] if len(witness) > 6 else None
            else:
                return [False, False, False, False]
        else:
            G = getattr(witness, 'G', None)
            X = getattr(witness, 'X', None)
            x = getattr(witness, 'x', None)
            y = getattr(witness, 'y', None)
            G_x = getattr(witness, 'G_x', None)
            G_y = getattr(witness, 'G_y', None)
            action = getattr(witness, 'action', None)
            
        if X is None and isinstance(G, PermutationGroup):
            X = list(range(G.degree))
            
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1 and X is not None:
            h2 = is_finite_transitive_action(G, X, action)
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1 and x is not None and y is not None:
            true_G_x = get_stabilizer(G, x, action)
            true_G_y = get_stabilizer(G, y, action)
            
            if true_G_x is not None and true_G_y is not None:
                if G_x is None:
                    G_x = true_G_x
                    G_x_ok = True
                else:
                    if isinstance(G_x, PermutationGroup) and isinstance(true_G_x, PermutationGroup):
                        G_x_ok = G_x.is_subgroup(true_G_x) and true_G_x.is_subgroup(G_x)
                    elif hasattr(G_x, 'elements') and hasattr(true_G_x, 'elements'):
                        try:
                            G_x_ok = set(G_x.elements) == set(true_G_x.elements)
                        except TypeError:
                            G_x_ok = all(e in true_G_x.elements for e in G_x.elements) and \
                                     all(e in G_x.elements for e in true_G_x.elements)
                    else:
                        G_x_ok = False
                        
                if G_y is None:
                    G_y = true_G_y
                    G_y_ok = True
                else:
                    if isinstance(G_y, PermutationGroup) and isinstance(true_G_y, PermutationGroup):
                        G_y_ok = G_y.is_subgroup(true_G_y) and true_G_y.is_subgroup(G_y)
                    elif hasattr(G_y, 'elements') and hasattr(true_G_y, 'elements'):
                        try:
                            G_y_ok = set(G_y.elements) == set(true_G_y.elements)
                        except TypeError:
                            G_y_ok = all(e in true_G_y.elements for e in G_y.elements) and \
                                     all(e in G_y.elements for e in true_G_y.elements)
                    else:
                        G_y_ok = False
                        
                if G_x_ok and G_y_ok:
                    h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2 and h3:
            def get_orbit(group, pt, act):
                if isinstance(group, PermutationGroup) and act is None:
                    if pt < group.degree:
                        return set(group.orbit(pt))
                    else:
                        return {pt}
                else:
                    orb = [pt]
                    q = [pt]
                    gens = group.generators if hasattr(group, 'generators') else group.elements
                    while q:
                        if len(orb) > 1000:
                            break
                        curr = q.pop(0)
                        for g in gens:
                            nxt = apply_action(g, curr, act)
                            if nxt not in orb:
                                orb.append(nxt)
                                q.append(nxt)
                    return orb

            orbit_y = get_orbit(G_x, y, action)
            orbit_x = get_orbit(G_y, x, action)
            
            neg_q = len(orbit_y) != len(orbit_x)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]