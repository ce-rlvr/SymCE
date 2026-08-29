import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

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
    identity = None
    try:
        if isinstance(witness, dict):
            G = witness.get('G', None)
            X = witness.get('X', None)
            Y = witness.get('Y', None)
            op_G = witness.get('op_G', None)
            action_X = witness.get('action_X', None)
            action_Y = witness.get('action_Y', None)
            phi = witness.get('phi', None)
        else:
            G = getattr(witness, 'G', None)
            X = getattr(witness, 'X', None)
            Y = getattr(witness, 'Y', None)
            op_G = getattr(witness, 'op_G', None)
            action_X = getattr(witness, 'action_X', None)
            action_Y = getattr(witness, 'action_Y', None)
            phi = getattr(witness, 'phi', None)
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1_ok = False
        if G is not None and op_G is not None and len(G) > 0:
            closed = True
            for g1 in G:
                for g2 in G:
                    if op_G(g1, g2) not in G:
                        closed = False
                        break
                if not closed: break
            
            if closed:
                assoc = True
                for g1 in G:
                    for g2 in G:
                        for g3 in G:
                            if op_G(op_G(g1, g2), g3) != op_G(g1, op_G(g2, g3)):
                                assoc = False
                                break
                        if not assoc: break
                    if not assoc: break
                
                if assoc:
                    for e in G:
                        is_e = True
                        for g in G:
                            if op_G(e, g) != g or op_G(g, e) != g:
                                is_e = False
                                break
                        if is_e:
                            identity = e
                            break
                    
                    if identity is not None:
                        inv = True
                        for g in G:
                            has_inv = False
                            for h in G:
                                if op_G(g, h) == identity and op_G(h, g) == identity:
                                    has_inv = True
                                    break
                            if not has_inv:
                                inv = False
                                break
                        h1_ok = inv
    except Exception:
        h1_ok = False

    # H2: X and Y are sets equipped with actions by G
    try:
        h2_ok = False
        if h1_ok and X is not None and Y is not None and action_X is not None and action_Y is not None:
            x_action_ok = True
            for g in G:
                for x in X:
                    if action_X(g, x) not in X:
                        x_action_ok = False
                        break
                if not x_action_ok: break
            
            if x_action_ok and identity is not None:
                for x in X:
                    if action_X(identity, x) != x:
                        x_action_ok = False
                        break
            
            if x_action_ok:
                for g in G:
                    for h in G:
                        for x in X:
                            if action_X(g, action_X(h, x)) != action_X(op_G(g, h), x):
                                x_action_ok = False
                                break
                        if not x_action_ok: break
                    if not x_action_ok: break
            
            y_action_ok = True
            for g in G:
                for y in Y:
                    if action_Y(g, y) not in Y:
                        y_action_ok = False
                        break
                if not y_action_ok: break
            
            if y_action_ok and identity is not None:
                for y in Y:
                    if action_Y(identity, y) != y:
                        y_action_ok = False
                        break
            
            if y_action_ok:
                for g in G:
                    for h in G:
                        for y in Y:
                            if action_Y(g, action_Y(h, y)) != action_Y(op_G(g, h), y):
                                y_action_ok = False
                                break
                        if not y_action_ok: break
                    if not y_action_ok: break
            
            h2_ok = x_action_ok and y_action_ok
    except Exception:
        h2_ok = False

    # H3: \phi: X \to Y is a bijection such that \phi(g \cdot x) = g \cdot \phi(x) for all g \in G and x \in X
    try:
        h3_ok = False
        if h2_ok and phi is not None:
            maps_to_Y = True
            for x in X:
                if phi(x) not in Y:
                    maps_to_Y = False
                    break
            
            if maps_to_Y:
                injective = True
                for x1 in X:
                    for x2 in X:
                        if x1 != x2 and phi(x1) == phi(x2):
                            injective = False
                            break
                    if not injective: break
                
                if injective:
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
                    
                    if surjective:
                        equiv = True
                        for g in G:
                            for x in X:
                                if phi(action_X(g, x)) != action_Y(g, phi(x)):
                                    equiv = False
                                    break
                            if not equiv: break
                        
                        h3_ok = equiv
    except Exception:
        h3_ok = False

    # Negated Conclusion: G_x != G_{\phi(x)}
    try:
        neg_q_ok = False
        if h2_ok and phi is not None:
            if isinstance(witness, dict) and 'x' in witness:
                x_list = [witness['x']]
            elif hasattr(witness, 'x'):
                x_list = [witness.x]
            else:
                x_list = X
                
            for x_elem in x_list:
                if x_elem not in X:
                    continue
                
                G_x = [g for g in G if action_X(g, x_elem) == x_elem]
                phi_x = phi(x_elem)
                G_phi_x = [g for g in G if action_Y(g, phi_x) == phi_x]
                
                subset1 = all(g in G_phi_x for g in G_x)
                subset2 = all(g in G_x for g in G_phi_x)
                
                if not (subset1 and subset2):
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are sets equipped with actions by G",
    "H_3: \\phi: X \\to Y is a bijection such that \\phi(g \\cdot x) = g \\cdot \\phi(x) for all g \\in G and x \\in X",
    "¬Q: The point stabilizer G_x is not equal to the point stabilizer G_{\\phi(x)}"
]

N_HYP = 3
NEG_Q_INDEX = 3