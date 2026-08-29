import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from math import gcd

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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The elements x and y commute",
    "H_3: The orders of x and y are relatively prime",
    "¬Q: C_G(xy) is not C_G(x) cap C_G(y) or class size is not the index"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False, False]

    try:
        if hasattr(G, 'order'):
            order_G = G.order() if callable(G.order) else G.order
            h1 = (order_G > 0 and order_G < float('inf'))
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = bool(x * y == y * x)
    except Exception:
        h2 = False

    try:
        def get_order(elem):
            if hasattr(elem, 'order'):
                return elem.order() if callable(elem.order) else elem.order
            raise ValueError("Order not found")
        
        ox = get_order(x)
        oy = get_order(y)
        h3 = bool(gcd(ox, oy) == 1)
    except Exception:
        h3 = False

    try:
        xy = x * y
        
        try:
            elements = list(G.elements)
        except Exception:
            try:
                elements = list(G.generate())
            except Exception:
                elements = list(G)
                
        C_xy = set()
        C_x = set()
        C_y = set()
        
        for g in elements:
            if g * xy == xy * g:
                C_xy.add(g)
            if g * x == x * g:
                C_x.add(g)
            if g * y == y * g:
                C_y.add(g)
                
        intersection = C_x.intersection(C_y)
        cond1 = (C_xy == intersection)
        
        conj_class = set()
        for g in elements:
            try:
                inv_g = ~g
            except Exception:
                inv_g = g**-1
            conj_class.add(g * xy * inv_g)
            
        cond2 = (len(conj_class) * len(intersection) == order_G)
        
        neg_Q = not (cond1 and cond2)
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]