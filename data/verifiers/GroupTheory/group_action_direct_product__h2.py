import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
    # H1: G is a group that acts on a set X
    def check_H1():
        try:
            G = witness['G']
            X = list(witness['X'])
            act_G = witness['act_G']
            
            if not hasattr(G, 'elements') or not hasattr(G, 'identity'):
                return False
                
            id_G = G.identity
            G_elements = list(G.elements)
            
            # Check identity action
            for x in X:
                if act_G(id_G, x) != x:
                    return False
                    
            # Check closure
            for g in G_elements:
                for x in X:
                    if act_G(g, x) not in X:
                        return False
                        
            # Check compatibility (left or right action)
            is_left = True
            is_right = True
            for g1 in G_elements:
                for g2 in G_elements:
                    g12 = g1 * g2
                    for x in X:
                        res12 = act_G(g12, x)
                        if res12 != act_G(g1, act_G(g2, x)):
                            is_left = False
                        if res12 != act_G(g2, act_G(g1, x)):
                            is_right = False
                        if not is_left and not is_right:
                            return False
            return is_left or is_right
        except Exception:
            return False

    # neg_Q: The direct product G x H does NOT act on X x Y via the component-wise action
    def check_neg_Q():
        try:
            G = witness['G']
            X = list(witness['X'])
            act_G = witness['act_G']
            H = witness['H']
            Y = list(witness['Y'])
            act_H = witness['act_H']
        except KeyError:
            return False

        try:
            # If H is not a group, G x H is not a group, so it cannot act.
            if not hasattr(H, 'elements') or not hasattr(H, 'identity'):
                return True
            
            id_G = G.identity
            G_elements = list(G.elements)
            id_H = H.identity
            H_elements = list(H.elements)
            
            GH_elements = [(g, h) for g in G_elements for h in H_elements]
            id_GH = (id_G, id_H)
            
            XY = [(x, y) for x in X for y in Y]
            
            def act_GH(gh, xy):
                return (act_G(gh[0], xy[0]), act_H(gh[1], xy[1]))
                
            # Check identity action
            for xy in XY:
                if act_GH(id_GH, xy) != xy:
                    return True
                    
            # Check closure
            for gh in GH_elements:
                for xy in XY:
                    if act_GH(gh, xy) not in XY:
                        return True
                        
            # Check compatibility
            is_left = True
            is_right = True
            for gh1 in GH_elements:
                for gh2 in GH_elements:
                    gh12 = (gh1[0] * gh2[0], gh1[1] * gh2[1])
                    for xy in XY:
                        res12 = act_GH(gh12, xy)
                        if res12 != act_GH(gh1, act_GH(gh2, xy)):
                            is_left = False
                        if res12 != act_GH(gh2, act_GH(gh1, xy)):
                            is_right = False
                        if not is_left and not is_right:
                            return True
            
            if is_left or is_right:
                return False
            return True
        except Exception:
            # If evaluation fails (e.g., act_H is undefined or raises an error), it's not a valid action.
            return True

    return [check_H1(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: G is a group that acts on a set X",
    "¬Q: The direct product G x H does not act on X x Y via the component-wise action"
]

N_HYP = 1
NEG_Q_INDEX = 1