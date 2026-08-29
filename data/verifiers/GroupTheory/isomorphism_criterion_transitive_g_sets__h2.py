import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    def apply_action(action, g, a):
        if callable(action):
            return action(g, a)
        elif isinstance(action, dict):
            return action[(g, a)]
        else:
            raise ValueError("Action must be callable or dict")

    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            Y = witness.get('Y')
            action_X = witness.get('action_X')
            action_Y = witness.get('action_Y')
            x = witness.get('x')
            y = witness.get('y')
        else:
            G = witness.G
            X = witness.X
            Y = witness.Y
            action_X = witness.action_X
            action_Y = witness.action_Y
            x = witness.x
            y = witness.y
    except Exception:
        return [False, False, False]

    # H1: G is a group and X, Y are valid G-sets
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements_G = list(G.elements)
            X_list = list(X)
            Y_list = list(Y)
            
            identity = None
            for g in elements_G:
                if g * g == g:
                    identity = g
                    break
            
            # Check action_X
            for a in X_list:
                if apply_action(action_X, identity, a) != a:
                    h1 = False
                    break
                for g in elements_G:
                    g_a = apply_action(action_X, g, a)
                    if g_a not in X_list:
                        h1 = False
                        break
                    for h in elements_G:
                        if apply_action(action_X, g*h, a) != apply_action(action_X, g, apply_action(action_X, h, a)):
                            h1 = False
                            break
                    if not h1: break
                if not h1: break
                
            # Check action_Y
            if h1:
                for a in Y_list:
                    if apply_action(action_Y, identity, a) != a:
                        h1 = False
                        break
                    for g in elements_G:
                        g_a = apply_action(action_Y, g, a)
                        if g_a not in Y_list:
                            h1 = False
                            break
                        for h in elements_G:
                            if apply_action(action_Y, g*h, a) != apply_action(action_Y, g, apply_action(action_Y, h, a)):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
    except Exception:
        h1 = False

    # H2: x in X and y in Y
    try:
        X_list = list(X)
        Y_list = list(Y)
        h2 = (x in X_list) and (y in Y_list)
    except Exception:
        h2 = False

    # neg_Q: X and Y are isomorphic as G-sets iff exists g in G such that g Stab_G(x) g^-1 == Stab_G(y)
    try:
        elements_G = list(G.elements)
        X_list = list(X)
        Y_list = list(Y)
        
        isomorphic = False
        if len(X_list) == len(Y_list):
            for p in itertools.permutations(Y_list):
                valid_iso = True
                for i, a in enumerate(X_list):
                    for g in elements_G:
                        g_a = apply_action(action_X, g, a)
                        idx_g_a = X_list.index(g_a)
                        f_g_a = p[idx_g_a]
                        
                        f_a = p[i]
                        g_f_a = apply_action(action_Y, g, f_a)
                        
                        if f_g_a != g_f_a:
                            valid_iso = False
                            break
                    if not valid_iso:
                        break
                if valid_iso:
                    isomorphic = True
                    break
                    
        stab_x = set()
        for g in elements_G:
            if apply_action(action_X, g, x) == x:
                stab_x.add(g)
                
        stab_y = set()
        for g in elements_G:
            if apply_action(action_Y, g, y) == y:
                stab_y.add(g)
                
        exists_g = False
        for g in elements_G:
            g_inv = g**-1
            conj = {g * s * g_inv for s in stab_x}
            if conj == stab_y:
                exists_g = True
                break
                
        neg_q = (isomorphic != exists_g)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and X, Y are valid G-sets",
    "H_2: x in X and y in Y",
    "¬Q: The equivalence between G-set isomorphism and conjugate stabilizers fails"
]

N_HYP = 2
NEG_Q_INDEX = 2