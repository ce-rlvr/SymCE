import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_cyclic(G):
    try:
        if hasattr(G, 'is_cyclic'):
            res = G.is_cyclic
            if isinstance(res, bool):
                return res
            if callable(res):
                return res()
    except Exception:
        pass
    
    try:
        order = G.order()
        if callable(order):
            order = order()
        for g in G.elements:
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def center_order(G):
    try:
        if hasattr(G, 'center'):
            C = G.center()
            if hasattr(C, 'order'):
                order = C.order() if callable(C.order) else C.order
                return order
            elif isinstance(C, list):
                return len(C)
    except Exception:
        pass
    
    c_order = 0
    try:
        gens = G.generators
        elements = list(G.elements)
        for g in elements:
            if all(g * h == h * g for h in gens):
                c_order += 1
        return c_order
    except Exception:
        pass
    return 1

def conditions(witness):
    try:
        h1_ok = False
        try:
            order = witness.order()
            if callable(order):
                order = order()
            # A group has rank >= 2 if and only if it is not cyclic (and not trivial).
            if order > 1 and not is_cyclic(witness):
                h1_ok = True
        except Exception:
            pass

        neg_q_ok = False
        try:
            # For finite groups, Inn(F) is isomorphic to F/Z(F).
            # Therefore, Inn(F) is isomorphic to F if and only if Z(F) is trivial.
            # The conclusion fails (neg_Q is True) if Z(F) is NOT trivial.
            c_order = center_order(witness)
            if c_order > 1:
                neg_q_ok = True
        except Exception:
            pass

        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: The rank of F is greater than or equal to 2",
    "¬Q: The group of inner automorphisms Inn(F) is not isomorphic to F"
]

N_HYP = 1
NEG_Q_INDEX = 1