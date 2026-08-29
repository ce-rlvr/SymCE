import sympy
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

def conditions(witness):
    try:
        G = list(witness['G'])
        X = list(witness['X'])
        Y = list(witness['Y'])
        
        if 'op' in witness:
            op_raw = witness['op']
            if isinstance(op_raw, dict):
                op = lambda g1, g2: op_raw.get((g1, g2))
            else:
                op = op_raw
        else:
            op = lambda g1, g2: g1 * g2
            
        if 'action_X' in witness:
            act_X_raw = witness['action_X']
            if isinstance(act_X_raw, dict):
                act_X = lambda g, x: act_X_raw.get((g, x))
            else:
                act_X = act_X_raw
        else:
            act_X = lambda g, x: g(x)
            
        if 'action_Y' in witness:
            act_Y_raw = witness['action_Y']
            if isinstance(act_Y_raw, dict):
                act_Y = lambda g, y: act_Y_raw.get((g, y))
            else:
                act_Y = act_Y_raw
        else:
            act_Y = lambda g, y: g(y)
            
        phi_raw = witness['phi']
        if isinstance(phi_raw, dict):
            phi = lambda x: phi_raw.get(x)
        else:
            phi = phi_raw

        # 1. Check if G is a group
        identity = None
        for e in G:
            if all(op(e, g) == g and op(g, e) == g for g in G):
                identity = e
                break
        
        is_group = False
        if identity is not None:
            closure = True
            for g1 in G:
                for g2 in G:
                    if op(g1, g2) not in G:
                        closure = False
                        break
                if not closure: break
            
            if closure:
                inverses = True
                for g in G:
                    has_inv = False
                    for inv in G:
                        if op(g, inv) == identity and op(inv, g) == identity:
                            has_inv = True
                            break
                    if not has_inv:
                        inverses = False
                        break
                
                if inverses:
                    associative = True
                    for g1 in G:
                        for g2 in G:
                            for g3 in G:
                                if op(op(g1, g2), g3) != op(g1, op(g2, g3)):
                                    associative = False
                                    break
                            if not associative: break
                        if not associative: break
                    
                    if associative:
                        is_group = True

        # Check action on X
        acts_on_X = True
        if not is_group:
            acts_on_X = False
        else:
            for x in X:
                if act_X(identity, x) != x:
                    acts_on_X = False
                    break
            if acts_on_X:
                for g in G:
                    for x in X:
                        if act_X(g, x) not in X:
                            acts_on_X = False
                            break
                    if not acts_on_X: break
            if acts_on_X:
                for g1 in G:
                    for g2 in G:
                        for x in X:
                            if act_X(g1, act_X(g2, x)) != act_X(op(g1, g2), x):
                                acts_on_X = False
                                break
                        if not acts_on_X: break
                    if not acts_on_X: break

        # Check transitivity on X
        transitive_X = True
        if acts_on_X and X:
            for x1 in X:
                for x2 in X:
                    reachable = False
                    for g in G:
                        if act_X(g, x1) == x2:
                            reachable = True
                            break
                    if not reachable:
                        transitive_X = False
                        break
                if not transitive_X: break
        else:
            transitive_X = False

        h1 = is_group and acts_on_X and transitive_X

        # Check action on Y
        acts_on_Y = True
        if not is_group:
            acts_on_Y = False
        else:
            for y in Y:
                if act_Y(identity, y) != y:
                    acts_on_Y = False
                    break
            if acts_on_Y:
                for g in G:
                    for y in Y:
                        if act_Y(g, y) not in Y:
                            acts_on_Y = False
                            break
                    if not acts_on_Y: break
            if acts_on_Y:
                for g1 in G:
                    for g2 in G:
                        for y in Y:
                            if act_Y(g1, act_Y(g2, y)) != act_Y(op(g1, g2), y):
                                acts_on_Y = False
                                break
                        if not acts_on_Y: break
                    if not acts_on_Y: break

        # Check transitivity on Y
        transitive_Y = True
        if acts_on_Y and Y:
            for y1 in Y:
                for y2 in Y:
                    reachable = False
                    for g in G:
                        if act_Y(g, y1) == y2:
                            reachable = True
                            break
                    if not reachable:
                        transitive_Y = False
                        break
                if not transitive_Y: break
        else:
            transitive_Y = False

        h2 = acts_on_Y and transitive_Y

        # Check if phi is surjective
        valid_phi = True
        for x in X:
            if phi(x) not in Y:
                valid_phi = False
                break
        
        if not valid_phi:
            neg_q = False
        else:
            surjective = True
            for y in Y:
                hit = False
                for x in X:
                    if phi(x) == y:
                        hit = True
                        break
                if not hit:
                    surjective = False
                    break
            neg_q = not surjective

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: G acts transitively on a non-empty set Y",
    "¬Q: The map phi is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2