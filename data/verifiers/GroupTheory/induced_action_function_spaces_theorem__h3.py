import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        def get_witness_attr(witness, attr):
            if isinstance(witness, dict):
                return witness[attr]
            else:
                return getattr(witness, attr)

        G = get_witness_attr(witness, 'G')
        mul = get_witness_attr(witness, 'mul')
        inv = get_witness_attr(witness, 'inv')
        e = get_witness_attr(witness, 'e')
        X = get_witness_attr(witness, 'X')
        Y = get_witness_attr(witness, 'Y')
        action = get_witness_attr(witness, 'action')
        
        G_list = list(G)
        X_list = list(X)
        Y_list = list(Y)
    except Exception:
        return [False, False, False]

    def get_val(f, *args):
        if callable(f):
            return f(*args)
        elif isinstance(f, dict):
            if len(args) == 1:
                return f[args[0]]
            else:
                return f[args]
        else:
            raise ValueError("Not callable or dict")

    # H1: G is a group acting on a set X
    h1_ok = True
    try:
        if e not in G_list: 
            h1_ok = False
        else:
            for g in G_list:
                if get_val(mul, e, g) != g or get_val(mul, g, e) != g: 
                    h1_ok = False
                    break
                g_inv = get_val(inv, g)
                if g_inv not in G_list: 
                    h1_ok = False
                    break
                if get_val(mul, g, g_inv) != e or get_val(mul, g_inv, g) != e: 
                    h1_ok = False
                    break
                for h in G_list:
                    gh = get_val(mul, g, h)
                    if gh not in G_list: 
                        h1_ok = False
                        break
                    for k in G_list:
                        if get_val(mul, gh, k) != get_val(mul, g, get_val(mul, h, k)): 
                            h1_ok = False
                            break
                    if not h1_ok: break
                if not h1_ok: break
        
        if h1_ok:
            for x in X_list:
                if get_val(action, e, x) != x: 
                    h1_ok = False
                    break
            
            if h1_ok:
                for g in G_list:
                    for x in X_list:
                        if get_val(action, g, x) not in X_list:
                            h1_ok = False
                            break
                    if not h1_ok: break

            if h1_ok:
                is_left = True
                is_right = True
                for g1 in G_list:
                    for g2 in G_list:
                        g1g2 = get_val(mul, g1, g2)
                        g2g1 = get_val(mul, g2, g1)
                        for x in X_list:
                            act_g2_x = get_val(action, g2, x)
                            act_g1_g2_x = get_val(action, g1, act_g2_x)
                            if act_g1_g2_x != get_val(action, g1g2, x):
                                is_left = False
                            if act_g1_g2_x != get_val(action, g2g1, x):
                                is_right = False
                if not (is_left or is_right):
                    h1_ok = False
    except Exception:
        h1_ok = False

    # H2: Y is a set
    h2_ok = True
    try:
        if not isinstance(Y, (list, set, tuple)):
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: The operation is NOT a valid group action of G on Y^X
    neg_q_ok = False
    try:
        if len(Y_list) ** len(X_list) > 10000:
            raise ValueError("Y^X too large")
            
        funcs = list(itertools.product(Y_list, repeat=len(X_list)))
        
        def induced_action(g, f):
            g_inv = get_val(inv, g)
            new_f = []
            for i, x in enumerate(X_list):
                inv_g_x = get_val(action, g_inv, x)
                idx = X_list.index(inv_g_x)
                new_f.append(f[idx])
            return tuple(new_f)
            
        is_valid_left = True
        
        for f in funcs:
            if induced_action(e, f) != f:
                is_valid_left = False
                break
                
        if is_valid_left:
            for g1 in G_list:
                for g2 in G_list:
                    g1g2 = get_val(mul, g1, g2)
                    for f in funcs:
                        act_g2_f = induced_action(g2, f)
                        act_g1_g2_f = induced_action(g1, act_g2_f)
                        if act_g1_g2_f != induced_action(g1g2, f):
                            is_valid_left = False
                            break
                    if not is_valid_left:
                        break
                if not is_valid_left:
                    break
                    
        neg_q_ok = not is_valid_left
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y is a set",
    "¬Q: The operation is not a valid group action of G on Y^X"
]

N_HYP = 2
NEG_Q_INDEX = 2