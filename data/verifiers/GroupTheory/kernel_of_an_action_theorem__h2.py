import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
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

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: G_x denotes the stabilizer of x in X in G",
    "¬Q: K is not a normal subgroup of G or K is not equal to the intersection of all stabilizers"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            action = witness.get('action')
            K = witness.get('K')
        else:
            G, X, action, K = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group acting on a set X
    h1 = False
    try:
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
            try:
                identity = G.identity
            except AttributeError:
                identity = None
                for e in G_elements:
                    if all(e * x == x and x * e == x for x in G_elements):
                        identity = e
                        break
        else:
            G_elements = list(G)
            identity = None
            for e in G_elements:
                if all(e * x == x and x * e == x for x in G_elements):
                    identity = e
                    break
        
        def mul(a, b): return a * b
        
        X_elements = list(X)
        
        if identity is not None:
            id_acts_trivially = True
            for x in X_elements:
                if action(identity, x) != x:
                    id_acts_trivially = False
                    break
            
            if id_acts_trivially:
                is_left_action = True
                is_right_action = True
                for g in G_elements:
                    for h in G_elements:
                        gh = mul(g, h)
                        for x in X_elements:
                            if action(g, action(h, x)) != action(gh, x):
                                is_left_action = False
                            if action(h, action(g, x)) != action(gh, x):
                                is_right_action = False
                            if not is_left_action and not is_right_action:
                                break
                        if not is_left_action and not is_right_action:
                            break
                    if not is_left_action and not is_right_action:
                        break
                if is_left_action or is_right_action:
                    h1 = True
    except Exception:
        h1 = False

    # H2: G_x denotes the stabilizer of x \in X in G.
    # We interpret this as requiring K to be a subset of G, as K is referenced in the conclusion.
    h2 = False
    try:
        K_elements = list(K)
        h2 = True
        for k in K_elements:
            if k not in G_elements:
                h2 = False
                break
    except Exception:
        h2 = False

    # Conclusion: K is a normal subgroup of G and is equal to the intersection \bigcap_{x \in X} G_x.
    neg_q = False
    try:
        intersection_Gx = []
        for g in G_elements:
            acts_trivially = True
            for x in X_elements:
                if action(g, x) != x:
                    acts_trivially = False
                    break
            if acts_trivially:
                intersection_Gx.append(g)
                
        is_subgroup = True
        if not K_elements:
            is_subgroup = False
        else:
            if identity not in K_elements:
                is_subgroup = False
            if is_subgroup:
                for k1 in K_elements:
                    for k2 in K_elements:
                        if mul(k1, k2) not in K_elements:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
        is_normal = is_subgroup
        if is_normal:
            for g in G_elements:
                for k in K_elements:
                    gk = mul(g, k)
                    if not any(gk == mul(k2, g) for k2 in K_elements):
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        same_elements = True
        for k in K_elements:
            if k not in intersection_Gx:
                same_elements = False
                break
        if same_elements:
            for g in intersection_Gx:
                if g not in K_elements:
                    same_elements = False
                    break
                    
        q = is_normal and same_elements
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]