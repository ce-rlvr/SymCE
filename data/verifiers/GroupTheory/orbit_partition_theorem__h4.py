import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, X, act = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            h1 = True
            try:
                G_elements = list(G.elements)
            except AttributeError:
                G_elements = list(G.generate())
        elif isinstance(G, (list, set, tuple)):
            G_elements = []
            for item in G:
                if item not in G_elements:
                    G_elements.append(item)
            if len(G_elements) > 0:
                identity = None
                for e in G_elements:
                    if all(e * x == x and x * e == x for x in G_elements):
                        identity = e
                        break
                if identity is not None:
                    h1 = True
                    for a in G_elements:
                        has_inv = False
                        for b in G_elements:
                            if a * b == identity and b * a == identity:
                                has_inv = True
                            if a * b not in G_elements:
                                h1 = False
                                break
                        if not has_inv or not h1:
                            h1 = False
                            break
        else:
            G_elements = list(G.elements)
            h1 = True
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple))
        if h2:
            X_list = []
            for item in X:
                if item not in X_list:
                    X_list.append(item)
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        if not (h1 and h2):
            h3 = False
        else:
            h3 = True
            for g in G_elements:
                for x in X_list:
                    val = act(g, x) if callable(act) else act[(g, x)]
                    if val not in X_list:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # neg_Q: ~ is not an equivalence relation, or its classes are not exactly the orbits
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            def rel(x, y):
                for g in G_elements:
                    val = act(g, x) if callable(act) else act[(g, x)]
                    if val == y:
                        return True
                return False
                
            is_equiv = True
            # Reflexive
            for x in X_list:
                if not rel(x, x):
                    is_equiv = False
                    break
            # Symmetric
            if is_equiv:
                for x in X_list:
                    for y in X_list:
                        if rel(x, y) and not rel(y, x):
                            is_equiv = False
                            break
                    if not is_equiv:
                        break
            # Transitive
            if is_equiv:
                for x in X_list:
                    for y in X_list:
                        for z in X_list:
                            if rel(x, y) and rel(y, z) and not rel(x, z):
                                is_equiv = False
                                break
                        if not is_equiv:
                            break
                    if not is_equiv:
                        break
            
            classes_eq_orbits = True
            if is_equiv:
                for x in X_list:
                    eq_class = []
                    for y in X_list:
                        if rel(x, y) and y not in eq_class:
                            eq_class.append(y)
                    
                    orbit = []
                    for g in G_elements:
                        val = act(g, x) if callable(act) else act[(g, x)]
                        if val not in orbit:
                            orbit.append(val)
                            
                    if len(eq_class) != len(orbit) or any(e not in orbit for e in eq_class):
                        classes_eq_orbits = False
                        break
                        
            neg_q = not (is_equiv and classes_eq_orbits)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "¬Q: The relation ~ is not an equivalence relation, or its equivalence classes are not the orbits"
]

N_HYP = 3
NEG_Q_INDEX = 3