import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def get_order(elem):
    """Helper function to determine the multiplicative order of an element."""
    if hasattr(elem, 'order'):
        if callable(elem.order):
            return int(elem.order())
        else:
            return int(elem.order)
    
    # Try matrix identity
    if hasattr(elem, 'shape') and hasattr(elem, 'is_Matrix') and elem.is_Matrix:
        I = eye(elem.shape[0])
        curr = elem
        for i in range(1, 2000):
            if curr == I:
                return i
            curr = curr * elem
            
    # Try **0 as identity
    try:
        I = elem**0
        curr = elem
        for i in range(1, 2000):
            if curr == I:
                return i
            curr = curr * elem
    except Exception:
        pass
        
    raise ValueError("Order not found or infinite")

def conditions(witness) -> list[bool]:
    try:
        G, x, y = witness
    except Exception:
        return [False] * 7

    # H_1: x is an element of G
    try:
        h1 = x in G
    except Exception:
        h1 = False

    # H_2: y is an element of G
    try:
        h2 = y in G
    except Exception:
        h2 = False

    # H_3: x and y commute
    try:
        h3 = (x * y == y * x)
    except Exception:
        h3 = False

    # H_4: x has finite order
    try:
        ox = get_order(x)
        h4 = (ox > 0)
    except Exception:
        h4 = False

    # H_5: y has finite order
    try:
        oy = get_order(y)
        h5 = (oy > 0)
    except Exception:
        h5 = False

    # H_6: The orders of x and y are coprime
    try:
        ox = get_order(x)
        oy = get_order(y)
        h6 = (math.gcd(ox, oy) == 1)
    except Exception:
        h6 = False

    # ¬Q: The centralizer of xy in G is NOT equal to the intersection of the centralizer of x in G and the centralizer of y in G
    try:
        xy = x * y
        if hasattr(G, 'centralizer'):
            C_xy = G.centralizer(xy)
            C_x = G.centralizer(x)
            C_y = G.centralizer(y)
            
            if hasattr(C_x, 'intersect'):
                C_x_cap_y = C_x.intersect(C_y)
            elif hasattr(C_x, 'intersection'):
                C_x_cap_y = C_x.intersection(C_y)
            else:
                C_x_cap_y = set(C_x.elements).intersection(set(C_y.elements))
                
            if hasattr(C_xy, 'is_subgroup') and hasattr(C_x_cap_y, 'is_subgroup'):
                c_holds = C_xy.is_subgroup(C_x_cap_y) and C_x_cap_y.is_subgroup(C_xy)
            else:
                set_xy = set(C_xy.elements) if hasattr(C_xy, 'elements') else set(C_xy)
                set_cap = set(C_x_cap_y.elements) if hasattr(C_x_cap_y, 'elements') else set(C_x_cap_y)
                c_holds = (set_xy == set_cap)
        else:
            # G is an iterable (e.g., list of matrices)
            C_xy = []
            for z in G:
                try:
                    if z * xy == xy * z:
                        C_xy.append(z)
                except Exception:
                    pass
                    
            C_x = []
            for z in G:
                try:
                    if z * x == x * z:
                        C_x.append(z)
                except Exception:
                    pass
                    
            C_y = []
            for z in G:
                try:
                    if z * y == y * z:
                        C_y.append(z)
                except Exception:
                    pass
            
            C_x_cap_y = []
            for z in C_x:
                for w in C_y:
                    if z == w:
                        C_x_cap_y.append(z)
                        break
                        
            c_holds = True
            for z in C_xy:
                found = False
                for w in C_x_cap_y:
                    if z == w:
                        found = True
                        break
                if not found:
                    c_holds = False
                    break
            if c_holds:
                for z in C_x_cap_y:
                    found = False
                    for w in C_xy:
                        if z == w:
                            found = True
                            break
                    if not found:
                        c_holds = False
                        break
                        
        neg_q = not c_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: y is an element of G",
    "H_3: x and y commute",
    "H_4: x has finite order",
    "H_5: y has finite order",
    "H_6: The orders of x and y are coprime",
    "¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G"
]

N_HYP = 6
NEG_Q_INDEX = 6