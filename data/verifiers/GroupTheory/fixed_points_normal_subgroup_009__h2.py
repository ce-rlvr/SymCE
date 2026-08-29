import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    def get_field(w, f, default=None):
        if isinstance(w, dict):
            return w.get(f, default)
        return getattr(w, f, default)

    # H1: G is a group
    try:
        G = get_field(witness, "G")
        h1 = isinstance(G, PermutationGroup) or (hasattr(G, "elements") and hasattr(G, "identity"))
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        G = get_field(witness, "G")
        X = get_field(witness, "X")
        action = get_field(witness, "action")
        
        id_G = G.identity
        h2_id = all(bool(action(id_G, x) == x) for x in X)
        
        is_left = True
        for g in G.elements:
            for h in G.elements:
                for x in X:
                    if bool(action(g*h, x) != action(g, action(h, x))):
                        is_left = False
                        break
                if not is_left: break
            if not is_left: break
            
        is_right = True
        for g in G.elements:
            for h in G.elements:
                for x in X:
                    if bool(action(g*h, x) != action(h, action(g, x))):
                        is_right = False
                        break
                if not is_right: break
            if not is_right: break
            
        h2 = h2_id and (is_left or is_right)
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        G = get_field(witness, "G")
        N = get_field(witness, "N")
        
        is_group_N = False
        if isinstance(N, PermutationGroup):
            is_group_N = True
        elif hasattr(N, "elements"):
            N_elems = list(N.elements)
            if G.identity in N_elems:
                is_group_N = True
                for a in N_elems:
                    if a**-1 not in N_elems:
                        is_group_N = False
                        break
                    for b in N_elems:
                        if a*b not in N_elems:
                            is_group_N = False
                            break
                    if not is_group_N: break
                    
        is_sub = True
        if is_group_N:
            G_elems = list(G.elements)
            for n in N.elements:
                if n not in G_elems:
                    is_sub = False
                    break
        else:
            is_sub = False
            
        is_norm = True
        if is_sub:
            N_elems = list(N.elements)
            for g in G.elements:
                g_inv = g**-1
                for n in N_elems:
                    if g * n * g_inv not in N_elems:
                        is_norm = False
                        break
                if not is_norm:
                    break
                    
        h3 = is_group_N and is_sub and is_norm
    except Exception:
        h3 = False

    # H4: X^N is the set of points in X fixed by every element of N
    try:
        X = get_field(witness, "X")
        N = get_field(witness, "N")
        action = get_field(witness, "action")
        
        expected_X_N = []
        for x in X:
            if all(bool(action(n, x) == x) for n in N.elements):
                expected_X_N.append(x)
                
        X_N_witness = get_field(witness, "X_N")
        if X_N_witness is not None:
            h4 = True
            for x in expected_X_N:
                if not any(bool(x == e) for e in X_N_witness):
                    h4 = False
                    break
            for x in X_N_witness:
                if not any(bool(x == e) for e in expected_X_N):
                    h4 = False
                    break
        else:
            h4 = True
    except Exception:
        h4 = False

    # neg_Q: The set X^N is NOT invariant under the action of G
    try:
        G = get_field(witness, "G")
        X = get_field(witness, "X")
        N = get_field(witness, "N")
        action = get_field(witness, "action")
        
        X_N_target = get_field(witness, "X_N")
        if X_N_target is None:
            X_N_target = []
            for x in X:
                if all(bool(action(n, x) == x) for n in N.elements):
                    X_N_target.append(x)
                    
        invariant = True
        for g in G.elements:
            for x in X_N_target:
                if not any(bool(action(g, x) == e) for e in X_N_target):
                    invariant = False
                    break
            if not invariant:
                break
        neg_q = not invariant
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "H_3: N is a normal subgroup of G",
    "H_4: X^N is the set of points in X fixed by every element of N",
    "¬Q: The set X^N is not invariant under the action of G"
]

N_HYP = 4
NEG_Q_INDEX = 4