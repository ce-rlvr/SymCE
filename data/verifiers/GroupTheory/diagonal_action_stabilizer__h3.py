import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_G_list(witness):
    G_obj = witness['G']
    if hasattr(G_obj, 'elements'):
        return list(G_obj.elements)
    elif hasattr(G_obj, 'generate'):
        return list(G_obj.generate())
    else:
        return list(G_obj)

def get_mul(witness):
    if 'mul' in witness:
        return witness['mul']
    return lambda a, b: a * b

def conditions(witness):
    # H1: G is a group acting on a set X and a set Y
    try:
        G = get_G_list(witness)
        X = list(witness['X'])
        Y = list(witness['Y'])
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        mul = get_mul(witness)
        
        if not G or not X or not Y:
            h1 = False
        else:
            e = None
            for cand in G:
                if all(mul(cand, g) == g and mul(g, cand) == g for g in G):
                    e = cand
                    break
            if e is None:
                h1 = False
            else:
                is_group = True
                for g1 in G:
                    has_inv = False
                    for g2 in G:
                        if mul(g1, g2) == e and mul(g2, g1) == e:
                            has_inv = True
                            break
                    if not has_inv:
                        is_group = False
                        break
                
                if is_group:
                    is_assoc = True
                    for g1 in G:
                        for g2 in G:
                            for g3 in G:
                                if mul(g1, mul(g2, g3)) != mul(mul(g1, g2), g3):
                                    is_assoc = False
                                    break
                            if not is_assoc: break
                        if not is_assoc: break
                    is_group = is_group and is_assoc
                
                acts_on_X = True
                for g in G:
                    for x in X:
                        if action_X(g, x) not in X:
                            acts_on_X = False
                            break
                    if not acts_on_X: break
                    
                if acts_on_X:
                    for x in X:
                        if action_X(e, x) != x:
                            acts_on_X = False
                            break
                            
                if acts_on_X:
                    for g1 in G:
                        for g2 in G:
                            for x in X:
                                if action_X(g1, action_X(g2, x)) != action_X(mul(g1, g2), x):
                                    acts_on_X = False
                                    break
                            if not acts_on_X: break
                        if not acts_on_X: break
                        
                acts_on_Y = True
                for g in G:
                    for y in Y:
                        if action_Y(g, y) not in Y:
                            acts_on_Y = False
                            break
                    if not acts_on_Y: break
                    
                if acts_on_Y:
                    for y in Y:
                        if action_Y(e, y) != y:
                            acts_on_Y = False
                            break
                            
                if acts_on_Y:
                    for g1 in G:
                        for g2 in G:
                            for y in Y:
                                if action_Y(g1, action_Y(g2, y)) != action_Y(mul(g1, g2), y):
                                    acts_on_Y = False
                                    break
                            if not acts_on_Y: break
                        if not acts_on_Y: break
                        
                h1 = is_group and acts_on_X and acts_on_Y
    except Exception:
        h1 = False

    # H2: G acts on the Cartesian product X \times Y via the diagonal action
    try:
        G = get_G_list(witness)
        X = list(witness['X'])
        Y = list(witness['Y'])
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        action_XY = witness['action_XY']
        mul = get_mul(witness)
        
        if not G or not X or not Y:
            h2 = False
        else:
            e = None
            for cand in G:
                if all(mul(cand, g) == g and mul(g, cand) == g for g in G):
                    e = cand
                    break
            if e is None:
                h2 = False
            else:
                acts_on_XY = True
                for g in G:
                    for x in X:
                        for y in Y:
                            res = action_XY(g, (x, y))
                            if not (isinstance(res, (tuple, list)) and len(res) == 2 and res[0] in X and res[1] in Y):
                                acts_on_XY = False
                                break
                        if not acts_on_XY: break
                    if not acts_on_XY: break
                    
                if acts_on_XY:
                    for x in X:
                        for y in Y:
                            if action_XY(e, (x, y)) != (x, y):
                                acts_on_XY = False
                                break
                        if not acts_on_XY: break
                
                if acts_on_XY:
                    for g1 in G:
                        for g2 in G:
                            for x in X:
                                for y in Y:
                                    if action_XY(g1, action_XY(g2, (x, y))) != action_XY(mul(g1, g2), (x, y)):
                                        acts_on_XY = False
                                        break
                                if not acts_on_XY: break
                            if not acts_on_XY: break
                        if not acts_on_XY: break
                        
                is_diagonal = True
                for g in G:
                    for x in X:
                        for y in Y:
                            if action_XY(g, (x, y)) != (action_X(g, x), action_Y(g, y)):
                                is_diagonal = False
                                break
                        if not is_diagonal: break
                    if not is_diagonal: break
                                
                h2 = acts_on_XY and is_diagonal
    except Exception:
        h2 = False

    # neg_Q: The stabilizer subgroup G_{(x, y)} is NOT equal to the intersection G_x \cap G_y
    try:
        G = get_G_list(witness)
        X = list(witness['X'])
        Y = list(witness['Y'])
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        action_XY = witness['action_XY']
        
        if 'x' in witness and 'y' in witness:
            pairs = [(witness['x'], witness['y'])]
        else:
            pairs = [(x, y) for x in X for y in Y]
            
        def lists_equal(l1, l2):
            for item in l1:
                if item not in l2: return False
            for item in l2:
                if item not in l1: return False
            return True
            
        conclusion_holds = True
        for x, y in pairs:
            Gx = [g for g in G if action_X(g, x) == x]
            Gy = [g for g in G if action_Y(g, y) == y]
            Gxy = [g for g in G if action_XY(g, (x, y)) == (x, y)]
            intersection = [g for g in Gx if g in Gy]
            
            if not lists_equal(Gxy, intersection):
                conclusion_holds = False
                break
                
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X and a set Y",
    "H_2: G acts on the Cartesian product X \\times Y via the diagonal action",
    "¬Q: The stabilizer subgroup G_{(x, y)} is not equal to the intersection G_x \\cap G_y"
]

N_HYP = 2
NEG_Q_INDEX = 2