import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    elif hasattr(group, 'generate'):
        return list(group.generate())
    else:
        elems = []
        for i, e in enumerate(group):
            if i > 2000:
                raise ValueError("Group too large")
            elems.append(e)
        return elems

def get_X_elements(X):
    elems = []
    for i, x in enumerate(X):
        if i > 2000:
            raise ValueError("Set X too large")
        elems.append(x)
    return elems

def get_identity(G_elems):
    if not G_elems:
        return None
    for e in G_elems:
        if all(e * g == g for g in G_elems) and all(g * e == g for g in G_elems):
            return e
    return None

def is_group(G):
    try:
        if hasattr(G, 'is_group') and G.is_group:
            return True
        if isinstance(G, PermutationGroup):
            return True
        elements = get_elements(G)
        if not elements:
            return False
        
        # Check closure
        for a in elements:
            for b in elements:
                if a * b not in elements:
                    return False
                    
        # Check identity
        e = get_identity(elements)
        if e is None:
            return False
            
        # Check inverses
        for a in elements:
            has_inv = False
            for b in elements:
                if a * b == e and b * a == e:
                    has_inv = True
                    break
            if not has_inv:
                return False
                
        # Check associativity for small groups
        if len(elements) < 50:
            for a in elements:
                for b in elements:
                    for c in elements:
                        if (a * b) * c != a * (b * c):
                            return False
        return True
    except Exception:
        return False

def is_set(X):
    try:
        return isinstance(X, (set, list, tuple, frozenset))
    except Exception:
        return False

def acts_on(G, X, action):
    try:
        elements = get_elements(G)
        X_list = get_X_elements(X)
        e = get_identity(elements)
        if e is None:
            return False
            
        # Check closure of action
        for g in elements:
            for x in X_list:
                if action(g, x) not in X_list:
                    return False

        # Check identity action
        for x in X_list:
            if action(e, x) != x:
                return False
                
        # Check compatibility
        for g in elements:
            for h in elements:
                for x in X_list:
                    if action(g, action(h, x)) != action(g * h, x):
                        return False
        return True
    except Exception:
        return False

def is_normal_subgroup(G, N):
    try:
        G_elems = get_elements(G)
        N_elems = get_elements(N)
        
        # Check subset
        for n in N_elems:
            if n not in G_elems:
                return False
                
        # Check subgroup
        e = get_identity(G_elems)
        if e not in N_elems:
            return False
        for a in N_elems:
            for b in N_elems:
                if a * b not in N_elems:
                    return False
                    
        # Check normality
        def get_inv(g):
            for h in G_elems:
                if g * h == e and h * g == e:
                    return h
            return None
            
        for g in G_elems:
            ginv = get_inv(g)
            if ginv is None:
                return False
            for n in N_elems:
                if g * n * ginv not in N_elems:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            action = witness.get('action')
            N = witness.get('N')
        else:
            G, X, action, N = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = is_set(X)
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = acts_on(G, X, action)
    except Exception:
        h3 = False

    # H4: N is a normal subgroup of G
    try:
        h4 = is_normal_subgroup(G, N)
    except Exception:
        h4 = False

    # Conclusion: The set X^N is invariant under the action of G.
    try:
        G_elems = get_elements(G)
        N_elems = get_elements(N)
        X_list = get_X_elements(X)
        
        # Find X^N (fixed points of N)
        fixed = []
        for x in X_list:
            if all(action(n, x) == x for n in N_elems):
                fixed.append(x)
        
        # Check invariance under G
        is_invariant = True
        for x in fixed:
            for g in G_elems:
                if action(g, x) not in fixed:
                    is_invariant = False
                    break
            if not is_invariant:
                break
        
        neg_q = not is_invariant
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "H_4: N is a normal subgroup of G",
    "¬Q: The set X^N is not invariant under the action of G"
]

N_HYP = 4
NEG_Q_INDEX = 4