import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    def get(attr):
        if isinstance(witness, dict):
            return witness.get(attr)
        return getattr(witness, attr, None)
    
    G = get('G')
    op = get('op')
    X = get('X')
    N = get('N')
    x = get('x')
    action = get('action')
    
    def mul(g1, g2):
        if op: return op(g1, g2)
        return g1 * g2

    try:
        G_list = list(G)
        X_list = list(X)
        N_list = list(N)
        
        # Find identity in G
        identity = None
        for e in G_list:
            if all(mul(e, g) == g and mul(g, e) == g for g in G_list):
                identity = e
                break
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group acting on a set X
    h1 = False
    try:
        if identity is not None:
            action_ok = True
            for y in X_list:
                if action(identity, y) != y:
                    action_ok = False
                    break
            if action_ok:
                for g in G_list:
                    for y in X_list:
                        if action(g, y) not in X_list:
                            action_ok = False
                            break
            if action_ok:
                for g1 in G_list:
                    for g2 in G_list:
                        for y in X_list:
                            if action(g1, action(g2, y)) != action(mul(g1, g2), y):
                                action_ok = False
                                break
            h1 = action_ok
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    h2 = False
    try:
        if identity in N_list:
            closure_ok = True
            for n1 in N_list:
                for n2 in N_list:
                    if mul(n1, n2) not in N_list:
                        closure_ok = False
            normal_ok = True
            for g in G_list:
                for n in N_list:
                    g_inv = None
                    for h in G_list:
                        if mul(g, h) == identity and mul(h, g) == identity:
                            g_inv = h
                            break
                    if g_inv is None or mul(mul(g, n), g_inv) not in N_list:
                        normal_ok = False
            h2 = closure_ok and normal_ok
    except Exception:
        h2 = False

    # H3: N acts trivially on X
    h3 = False
    try:
        triv = True
        for n in N_list:
            for y in X_list:
                if action(n, y) != y:
                    triv = False
                    break
        h3 = triv
    except Exception:
        h3 = False

    # H4: G/N acts on X via the induced action (gN) \cdot x = g \cdot x
    h4 = False
    try:
        well_defined = True
        for g1 in G_list:
            for g2 in G_list:
                g1_inv = None
                for h in G_list:
                    if mul(g1, h) == identity and mul(h, g1) == identity:
                        g1_inv = h
                        break
                if g1_inv is not None and mul(g1_inv, g2) in N_list:
                    for y in X_list:
                        if action(g1, y) != action(g2, y):
                            well_defined = False
        h4 = well_defined
    except Exception:
        h4 = False

    # Conclusion: The stabilizer of x in G/N is the quotient group G_x/N
    neg_q = False
    try:
        G_x = []
        for g in G_list:
            if action(g, x) == x:
                G_x.append(g)
        
        gx_is_subgroup = True
        if identity not in G_x:
            gx_is_subgroup = False
        else:
            for g1 in G_x:
                for g2 in G_x:
                    if mul(g1, g2) not in G_x:
                        gx_is_subgroup = False
                        break

        n_in_Gx = all(n in G_x for n in N_list)
        
        action_x_well_defined = True
        for g1 in G_list:
            for g2 in G_list:
                g1_inv = None
                for h in G_list:
                    if mul(g1, h) == identity and mul(h, g1) == identity:
                        g1_inv = h
                        break
                if g1_inv is not None and mul(g1_inv, g2) in N_list:
                    if action(g1, x) != action(g2, x):
                        action_x_well_defined = False
                        
        if not gx_is_subgroup or not n_in_Gx or not action_x_well_defined:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N is a normal subgroup of G",
    "H_3: N acts trivially on X",
    "H_4: G/N acts on X via the induced action",
    "¬Q: The stabilizer of x in G/N is not the quotient group G_x/N"
]

N_HYP = 4
NEG_Q_INDEX = 4