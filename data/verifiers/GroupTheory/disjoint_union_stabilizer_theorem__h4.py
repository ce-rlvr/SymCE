import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
        G_obj = witness['G']
        X = set(witness['X'])
        Y = set(witness['Y'])
        x = witness['x']
    except Exception:
        return [False] * 4 + [False]

    # H1: G is a group
    try:
        if hasattr(G_obj, 'is_group') and G_obj.is_group:
            if hasattr(G_obj, 'elements'):
                G = list(G_obj.elements)
            else:
                G = list(G_obj.generate())
            def mult(g, h): return g * h
            e = G_obj.identity
            h1 = True
        else:
            G = list(G_obj)
            mult_dict = witness['mult']
            def mult(g, h):
                if callable(mult_dict): return mult_dict(g, h)
                return mult_dict[(g, h)]
            
            h1 = True
            for g in G:
                for h in G:
                    if mult(g, h) not in G: h1 = False
            if h1:
                for g in G:
                    for h in G:
                        for k in G:
                            if mult(mult(g, h), k) != mult(g, mult(h, k)): h1 = False
            e = None
            if h1:
                for cand in G:
                    if all(mult(cand, g) == g and mult(g, cand) == g for g in G):
                        e = cand
                        break
                if e is None: h1 = False
            if h1:
                for g in G:
                    if not any(mult(g, h) == e and mult(h, g) == e for h in G): h1 = False
    except Exception:
        h1 = False

    # Setup actions
    try:
        if 'act_X' in witness:
            act_X_dict = witness['act_X']
            def act_X(g, s):
                if callable(act_X_dict): return act_X_dict(g, s)
                return act_X_dict[(g, s)]
        else:
            def act_X(g, s): return g(s)
            
        if 'act_Y' in witness:
            act_Y_dict = witness['act_Y']
            def act_Y(g, s):
                if callable(act_Y_dict): return act_Y_dict(g, s)
                return act_Y_dict[(g, s)]
        else:
            def act_Y(g, s): return g(s)
    except Exception:
        pass

    def check_action(S, act):
        for s in S:
            if act(e, s) != s: return False
        is_left = True
        is_right = True
        for g in G:
            for h in G:
                gh = mult(g, h)
                for s in S:
                    try:
                        val_g = act(g, s)
                        if val_g not in S: return False
                        val_h = act(h, s)
                        if val_h not in S: return False
                        
                        if act(g, val_h) != act(gh, s): is_left = False
                        if act(h, val_g) != act(gh, s): is_right = False
                    except Exception:
                        return False
        return is_left or is_right

    # H2: X and Y are disjoint sets
    try:
        h2 = X.isdisjoint(Y)
    except Exception:
        h2 = False

    # H3: G acts on X and G acts on Y
    try:
        h3 = False
        if h1:
            h3 = check_action(X, act_X) and check_action(Y, act_Y)
    except Exception:
        h3 = False

    # H4: x is an element of X
    try:
        h4 = x in X
    except Exception:
        h4 = False

    # Conclusion: The stabilizer of x under the action of G on X \sqcup Y 
    # is equal to the stabilizer of x under the action of G on X.
    try:
        if 'act_XY' in witness:
            act_XY_dict = witness['act_XY']
            def act_XY(g, s):
                if callable(act_XY_dict): return act_XY_dict(g, s)
                return act_XY_dict[(g, s)]
        else:
            def act_XY(g, s):
                if s in X: return act_X(g, s)
                if s in Y: return act_Y(g, s)
                return s

        stab_X = set()
        for g in G:
            if act_X(g, x) == x:
                stab_X.add(g)
                
        stab_XY = set()
        for g in G:
            if act_XY(g, x) == x:
                stab_XY.add(g)
                
        neg_q = (stab_X != stab_XY)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are disjoint sets",
    "H_3: G acts on X and G acts on Y",
    "H_4: x is an element of X",
    "¬Q: The stabilizer of x under the action of G on X \\sqcup Y is NOT equal to the stabilizer of x under the action of G on X"
]

N_HYP = 4
NEG_Q_INDEX = 4