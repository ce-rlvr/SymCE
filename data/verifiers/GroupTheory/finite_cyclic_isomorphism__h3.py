import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy.matrices import eye, zeros

# Standard finite groups
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Infinite cyclic group (the counterexample)
class InfiniteCyclicGroup:
    is_group = True
    is_cyclic = True
    generators = ['x']
    
    def order(self):
        return sympy.oo

Z = InfiniteCyclicGroup()

def check_H1(G):
    try:
        is_grp_attr = getattr(G, 'is_group', None)
        if is_grp_attr is not None:
            if callable(is_grp_attr):
                if is_grp_attr():
                    return True
            else:
                if is_grp_attr:
                    return True
                    
        if type(G).__name__ in ['FreeGroup', 'FpGroup', 'PermutationGroup', 'AlternatingGroup', 'SymmetricGroup', 'CyclicGroup', 'DihedralGroup']:
            return True
            
        if hasattr(G, 'generators') and hasattr(G, 'order'):
            return True
            
        return False
    except Exception:
        return False

def check_H2(G):
    try:
        is_cyc_attr = getattr(G, 'is_cyclic', None)
        if is_cyc_attr is not None:
            if callable(is_cyc_attr):
                try:
                    if is_cyc_attr():
                        return True
                except Exception:
                    pass
            else:
                if is_cyc_attr:
                    return True
                    
        if type(G).__name__ == 'FreeGroup':
            return len(G.generators) == 1
            
        if isinstance(G, InfiniteCyclicGroup):
            return True
            
        if hasattr(G, 'generators') and len(G.generators) == 1:
            return True
            
        try:
            order = G.order() if callable(G.order) else G.order
        except Exception:
            order = sympy.oo
            
        if order == sympy.oo or order == float('inf') or order is None:
            return False
            
        for g in G.elements:
            g_order = g.order() if callable(g.order) else g.order
            if g_order == order:
                return True
        return False
    except Exception:
        return False

def check_neg_Q(G):
    try:
        is_finite = False
        order = None
        if isinstance(G, InfiniteCyclicGroup):
            is_finite = False
        elif type(G).__name__ == 'FreeGroup' and len(G.generators) > 0:
            is_finite = False
        else:
            try:
                if hasattr(G, 'order'):
                    order = G.order() if callable(G.order) else G.order
                    if order != sympy.oo and order != float('inf') and order is not None:
                        is_finite = True
            except Exception:
                is_finite = False
                
        if not is_finite:
            return True
            
        is_cyc = False
        is_cyc_attr = getattr(G, 'is_cyclic', None)
        if is_cyc_attr is not None:
            if callable(is_cyc_attr):
                try:
                    if is_cyc_attr():
                        is_cyc = True
                except Exception:
                    pass
            else:
                if is_cyc_attr:
                    is_cyc = True
                    
        if not is_cyc:
            try:
                for g in G.elements:
                    g_order = g.order() if callable(g.order) else g.order
                    if g_order == order:
                        is_cyc = True
                        break
            except Exception:
                pass
                
        return not is_cyc
    except Exception:
        return False

def conditions(witness):
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is cyclic",
    "¬Q: G is not isomorphic to Z_n for any n"
]

N_HYP = 2
NEG_Q_INDEX = 2