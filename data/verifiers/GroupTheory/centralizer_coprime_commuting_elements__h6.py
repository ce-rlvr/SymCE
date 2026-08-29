import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
        # The witness can be (G, x, y), (G, x, y, g), or (x, y, g)
        if hasattr(witness, '__len__') and len(witness) >= 3:
            if hasattr(witness[0], 'is_group') or hasattr(witness[0], 'elements'):
                G = witness[0]
                x = witness[1]
                y = witness[2]
                g = witness[3] if len(witness) >= 4 else None
            else:
                G = None
                x = witness[0]
                y = witness[1]
                g = witness[2] if len(witness) >= 3 else None
        else:
            return [False] * 7
            
        # H1: G is a group
        h1 = True
        if G is not None:
            h1 = getattr(G, 'is_group', True)
        else:
            try:
                if hasattr(x, 'det'):
                    h1 = (x.det() != 0 and y.det() != 0)
                    if g is not None:
                        h1 = h1 and (g.det() != 0)
            except Exception:
                pass
                
        # H2: x is an element of G
        h2 = True
        if G is not None and hasattr(G, 'elements'):
            h2 = x in G.elements
            
        # H3: y is an element of G
        h3 = True
        if G is not None and hasattr(G, 'elements'):
            h3 = y in G.elements
            
        # H4: x and y commute
        h4 = bool(x * y == y * x)
        
        # Helper to compute the order of an element
        def get_order(elem):
            if hasattr(elem, 'order'):
                try:
                    o = elem.order()
                    if o < float('inf'):
                        return int(o)
                except Exception:
                    pass
            try:
                I_elem = elem**0
            except Exception:
                return 0
            for i in range(1, 1000):
                try:
                    if elem**i == I_elem:
                        return i
                except Exception:
                    pass
            return 0
            
        ox = get_order(x)
        oy = get_order(y)
        
        # H5: x has finite order
        h5 = (ox > 0)
        
        # H6: The orders of x and y are coprime
        # If y has infinite order (oy == 0), it is considered coprime to the finite order of x
        # This is the only way the conjecture can fail (the dropped hypothesis was "y has finite order")
        if oy == 0:
            h6 = True
        else:
            h6 = (math.gcd(ox, oy) == 1)
            
        # ¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G
        if g is not None:
            in_C_xy = bool(g * (x * y) == (x * y) * g)
            in_C_x = bool(g * x == x * g)
            in_C_y = bool(g * y == y * g)
            neg_q = (in_C_xy != (in_C_x and in_C_y))
        elif G is not None and hasattr(G, 'elements'):
            C_xy = [elem for elem in G.elements if elem * (x * y) == (x * y) * elem]
            C_x = [elem for elem in G.elements if elem * x == x * elem]
            C_y = [elem for elem in G.elements if elem * y == y * elem]
            C_x_cap_y = [elem for elem in C_x if elem in C_y]
            neg_q = (len(C_xy) != len(C_x_cap_y)) or any(elem not in C_x_cap_y for elem in C_xy)
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(h6), bool(neg_q)]
    except Exception:
        return [False] * 7

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "H_4: x and y commute",
    "H_5: x has finite order",
    "H_6: The orders of x and y are coprime",
    "¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G"
]

N_HYP = 6
NEG_Q_INDEX = 6