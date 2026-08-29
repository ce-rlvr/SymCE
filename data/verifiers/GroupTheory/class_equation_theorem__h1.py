import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: R is a set of representatives for the distinct conjugacy classes of G that are not contained in Z(G)",
    "not_Q: The order of G is not equal to the order of Z(G) plus the sum over all x in R of the index of C_G(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_center(G):
    if hasattr(G, 'center'):
        attr = getattr(G, 'center')
        if callable(attr):
            return attr()
        return attr
    elif hasattr(G, 'Z'):
        attr = getattr(G, 'Z')
        if callable(attr):
            return attr()
        return attr
    raise ValueError("No center found")

def get_conjugacy_classes(G):
    if hasattr(G, 'conjugacy_classes'):
        attr = getattr(G, 'conjugacy_classes')
        if callable(attr):
            return attr()
        return attr
    raise ValueError("No conjugacy_classes found")

def get_order(obj):
    if hasattr(obj, 'order'):
        attr = getattr(obj, 'order')
        if callable(attr):
            return attr()
        return attr
    return len(obj)

def get_centralizer(G, x):
    if hasattr(G, 'centralizer'):
        attr = getattr(G, 'centralizer')
        if callable(attr):
            return attr(x)
        return attr[x]
    elif hasattr(G, 'C_G'):
        attr = getattr(G, 'C_G')
        if callable(attr):
            return attr(x)
        return attr[x]
    raise ValueError("No centralizer found")

def conditions(witness):
    try:
        if len(witness) == 3:
            G, Z_G, R = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: Z(G) is the center of G
    try:
        center = get_center(G)
        if Z_G == center or Z_G is center:
            h1 = True
        elif hasattr(Z_G, 'is_subgroup') and hasattr(center, 'is_subgroup'):
            h1 = bool(Z_G.is_subgroup(center) and center.is_subgroup(Z_G))
        elif hasattr(Z_G, 'elements') and hasattr(center, 'elements'):
            h1 = bool(set(Z_G.elements) == set(center.elements))
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: R is a set of representatives for the distinct conjugacy classes of G that are not contained in Z(G)
    try:
        classes = get_conjugacy_classes(G)
        non_central_classes = []
        for c in classes:
            try:
                if hasattr(c, 'elements'):
                    c_elems = list(c.elements)
                else:
                    c_elems = list(c)
            except Exception:
                continue
                
            if not c_elems:
                continue
                
            rep = c_elems[0]
            
            in_Z = False
            if hasattr(Z_G, 'contains'):
                in_Z = Z_G.contains(rep)
            elif hasattr(Z_G, 'elements'):
                in_Z = rep in Z_G.elements
            else:
                in_Z = rep in Z_G
                
            if not in_Z:
                non_central_classes.append(c_elems)
                
        if len(R) != len(non_central_classes):
            h2 = False
        else:
            h2 = True
            for c_elems in non_central_classes:
                count = 0
                for x in R:
                    if x in c_elems:
                        count += 1
                if count != 1:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # neg_Q: The order of G is not equal to the order of Z(G) plus the sum over all x in R of the index of C_G(x) in G
    try:
        order_G = get_order(G)
        order_Z = get_order(Z_G)
        
        sum_index = 0
        for x in R:
            C_Gx = get_centralizer(G, x)
            order_C = get_order(C_Gx)
            
            if hasattr(G, 'index') and callable(getattr(G, 'index')):
                try:
                    index = G.index(C_Gx)
                except Exception:
                    index = order_G / order_C
            else:
                try:
                    if order_G % order_C == 0:
                        index = order_G // order_C
                    else:
                        index = order_G / order_C
                except Exception:
                    index = order_G / order_C
                    
            sum_index += index
            
        conclusion = (order_G == order_Z + sum_index)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]