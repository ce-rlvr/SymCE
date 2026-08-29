import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: Let x and y be elements of G
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
        h1 = (x in elements) and (y in elements)
    except Exception:
        h1 = False
        
    # H2: The elements x and y commute
    try:
        h2 = (x * y == y * x)
    except Exception:
        h2 = False
        
    # H3: The orders of x and y are relatively prime
    try:
        def get_order(elem):
            if hasattr(elem, 'order'):
                if callable(elem.order):
                    return elem.order()
                return elem.order
            raise ValueError("No order attribute")
        h3 = math.gcd(get_order(x), get_order(y)) == 1
    except Exception:
        h3 = False
        
    # Conclusion:
    # C_G(xy) == C_G(x) \cap C_G(y)
    # size of conjugacy class of xy in G == index of C_G(x) \cap C_G(y) in G
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        C_xy = {g for g in elements if g * (x * y) == (x * y) * g}
        C_x = {g for g in elements if g * x == x * g}
        C_y = {g for g in elements if g * y == y * g}
        
        intersection = C_x.intersection(C_y)
        part1 = (C_xy == intersection)
        
        conj_class = set()
        for g in elements:
            inv = None
            try:
                inv = ~g
            except Exception:
                try:
                    inv = g**-1
                except Exception:
                    pass
            if inv is not None:
                conj_class.add(g * (x * y) * inv)
                
        conj_class_size = len(conj_class)
        
        if len(intersection) == 0:
            part2 = False
        else:
            index = len(elements) // len(intersection)
            part2 = (conj_class_size == index)
            
        Q = part1 and part2
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: Let x and y be elements of G",
    "H_2: The elements x and y commute",
    "H_3: The orders of x and y are relatively prime",
    "¬Q: The centralizer C_G(xy) is not equal to C_G(x) intersection C_G(y), or the size of the conjugacy class of xy is not the index of C_G(x) intersection C_G(y) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3