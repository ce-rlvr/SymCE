import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G', [])
            op = witness.get('op', lambda a, b: a * b)
            X = witness.get('X', [])
            Y = witness.get('Y', [])
            action_X = witness.get('action_X')
            action_Y = witness.get('action_Y')
            f = witness.get('f')
            x_target = witness.get('x')
        else:
            G = getattr(witness, 'G', [])
            op = getattr(witness, 'op', lambda a, b: a * b)
            X = getattr(witness, 'X', [])
            Y = getattr(witness, 'Y', [])
            action_X = getattr(witness, 'action_X')
            action_Y = getattr(witness, 'action_Y')
            f = getattr(witness, 'f')
            x_target = getattr(witness, 'x')
    except Exception:
        return [False, False, False, False]

    # H1: G is a group acting on sets X and Y
    h1_ok = False
    try:
        if hasattr(G, 'elements'):
            G_list = list(G.elements)
        else:
            G_list = list(G)
            
        X_list = list(X)
        Y_list = list(Y)
        
        if G_list:
            # Find identity
            identities = []
            for e in G_list:
                if all(op(e, g) == g and op(g, e) == g for g in G_list):
                    identities.append(e)
            if len(identities) == 1:
                e = identities[0]
                # Check inverses
                inverses_ok = True
                for g in G_list:
                    if not any(op(g, h) == e and op(h, g) == e for h in G_list):
                        inverses_ok = False
                        break
                # Check associativity
                assoc_ok = True
                for g1, g2, g3 in itertools.product(G_list, repeat=3):
                    if op(op(g1, g2), g3) != op(g1, op(g2, g3)):
                        assoc_ok = False
                        break
                
                if inverses_ok and assoc_ok:
                    # Check action on X
                    action_X_ok = True
                    for x in X_list:
                        if action_X(e, x) != x:
                            action_X_ok = False
                            break
                        for g in G_list:
                            if action_X(g, x) not in X_list:
                                action_X_ok = False
                                break
                        if not action_X_ok:
                            break
                        for g1, g2 in itertools.product(G_list, repeat=2):
                            if action_X(g1, action_X(g2, x)) != action_X(op(g1, g2), x):
                                action_X_ok = False
                                break
                        if not action_X_ok:
                            break
                    
                    # Check action on Y
                    action_Y_ok = True
                    for y in Y_list:
                        if action_Y(e, y) != y:
                            action_Y_ok = False
                            break
                        for g in G_list:
                            if action_Y(g, y) not in Y_list:
                                action_Y_ok = False
                                break
                        if not action_Y_ok:
                            break
                        for g1, g2 in itertools.product(G_list, repeat=2):
                            if action_Y(g1, action_Y(g2, y)) != action_Y(op(g1, g2), y):
                                action_Y_ok = False
                                break
                        if not action_Y_ok:
                            break
                    
                    h1_ok = action_X_ok and action_Y_ok
    except Exception:
        h1_ok = False

    # H2: f is a bijection from X to Y
    h2_ok = False
    try:
        if len(X_list) == len(Y_list):
            f_X = []
            for x in X_list:
                fx = f(x)
                if fx not in Y_list:
                    break
                f_X.append(fx)
            else:
                # Check injectivity
                unique_f_X = []
                for fx in f_X:
                    if fx not in unique_f_X:
                        unique_f_X.append(fx)
                if len(unique_f_X) == len(X_list):
                    h2_ok = True
    except Exception:
        h2_ok = False

    # H3: f is G-equivariant on X
    h3_ok = False
    try:
        h3_ok = True
        for g in G_list:
            for x in X_list:
                if f(action_X(g, x)) != action_Y(g, f(x)):
                    h3_ok = False
                    break
            if not h3_ok:
                break
    except Exception:
        h3_ok = False

    # neg_Q: Stab(x) != Stab(f(x))
    neg_q = False
    try:
        stab_x_indices = set()
        for i, g in enumerate(G_list):
            if action_X(g, x_target) == x_target:
                stab_x_indices.add(i)
        
        fx_target = f(x_target)
        stab_fx_indices = set()
        for i, g in enumerate(G_list):
            if action_Y(g, fx_target) == fx_target:
                stab_fx_indices.add(i)
        
        neg_q = (stab_x_indices != stab_fx_indices)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on sets X and Y",
    "H_2: f is a bijection from X to Y",
    "H_3: f is G-equivariant on X",
    "¬Q: The stabilizer of x in G is not equal to the stabilizer of f(x) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3