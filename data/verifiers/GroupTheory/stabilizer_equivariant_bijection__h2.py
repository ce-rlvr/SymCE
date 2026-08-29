import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi: X -> Y is a bijection such that phi(g.x) = g.phi(x) for all g in G, x in X",
    "H_3: x is an element of X",
    "¬Q: The point stabilizer G_x is not equal to the point stabilizer G_{phi(x)}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            Y = witness['Y']
            phi = witness['phi']
            action_X = witness['action_X']
            action_Y = witness['action_Y']
            x_elem = witness['x']
            op = witness.get('op', None)
        else:
            G = witness.G
            X = witness.X
            Y = witness.Y
            phi = witness.phi
            action_X = witness.action_X
            action_Y = witness.action_Y
            x_elem = witness.x
            op = getattr(witness, 'op', None)
    except Exception:
        return [False, False, False, False]

    def apply_map(f, *args):
        if callable(f):
            return f(*args)
        elif isinstance(f, dict):
            if len(args) == 1:
                return f[args[0]]
            else:
                return f[args]
        else:
            raise TypeError("Mapping must be callable or dict")

    # H1: G is a group
    h1 = False
    G_elements = []
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
            G_elements = list(G.generate())
        else:
            G_elements = list(G)
            if not G_elements:
                h1 = False
            else:
                if op is None:
                    if all(isinstance(g, Permutation) for g in G_elements):
                        op = lambda a, b: a * b
                if op is not None:
                    closed = True
                    for a in G_elements:
                        for b in G_elements:
                            if op(a, b) not in G_elements:
                                closed = False
                                break
                        if not closed:
                            break
                    if closed:
                        assoc = True
                        for a in G_elements:
                            for b in G_elements:
                                for c in G_elements:
                                    if op(op(a, b), c) != op(a, op(b, c)):
                                        assoc = False
                                        break
                                if not assoc: break
                            if not assoc: break
                        if assoc:
                            for e in G_elements:
                                if all(op(e, a) == a and op(a, e) == a for a in G_elements):
                                    has_invs = True
                                    for a in G_elements:
                                        if not any(op(a, b) == e and op(b, a) == e for b in G_elements):
                                            has_invs = False
                                            break
                                    if has_invs:
                                        h1 = True
                                        break
    except Exception:
        h1 = False

    # H2: phi is a bijection from X to Y and equivariant
    h2 = False
    try:
        X_list = list(X)
        Y_list = list(Y)
        
        mapped_X = []
        for a in X_list:
            mapped_X.append(apply_map(phi, a))
            
        maps_into_Y = True
        for y in mapped_X:
            if y not in Y_list:
                maps_into_Y = False
                break
                
        is_injective = True
        for i in range(len(mapped_X)):
            for j in range(i + 1, len(mapped_X)):
                if mapped_X[i] == mapped_X[j]:
                    is_injective = False
                    break
            if not is_injective:
                break
                
        is_surjective = True
        for y in Y_list:
            if y not in mapped_X:
                is_surjective = False
                break
        if len(mapped_X) != len(Y_list):
            is_surjective = False
            
        is_bijection = maps_into_Y and is_injective and is_surjective
        
        if is_bijection:
            is_equivariant = True
            for g in G_elements:
                for a in X_list:
                    left = apply_map(phi, apply_map(action_X, g, a))
                    right = apply_map(action_Y, g, apply_map(phi, a))
                    if left != right:
                        is_equivariant = False
                        break
                if not is_equivariant:
                    break
            if is_equivariant:
                h2 = True
    except Exception:
        h2 = False

    # H3: x is an element of X
    h3 = False
    try:
        for a in list(X):
            if a == x_elem:
                h3 = True
                break
    except Exception:
        h3 = False

    # neg_Q: G_x != G_phi_x
    neg_q = False
    try:
        G_x = []
        for g in G_elements:
            if apply_map(action_X, g, x_elem) == x_elem:
                G_x.append(g)
                
        G_phi_x = []
        phi_x = apply_map(phi, x_elem)
        for g in G_elements:
            if apply_map(action_Y, g, phi_x) == phi_x:
                G_phi_x.append(g)
                
        def is_subset(A, B):
            for a in A:
                if a not in B:
                    return False
            return True
            
        if not (is_subset(G_x, G_phi_x) and is_subset(G_phi_x, G_x)):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]