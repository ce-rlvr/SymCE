import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def get_order(elem, group=None):
    """Helper to find the order of an element in a group."""
    try:
        return elem.order()
    except Exception:
        pass
    try:
        return elem.order
    except Exception:
        pass
    
    curr = elem
    for i in range(1, 2000):
        if group is not None and hasattr(group, 'identity') and curr == group.identity:
            return i
        if hasattr(curr, 'is_Identity') and curr.is_Identity:
            return i
        try:
            if curr == elem**0:
                return i
        except Exception:
            pass
        curr = curr * elem
    return float('inf')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            x = witness.get('x')
        else:
            G, H, f, x = witness
    except Exception:
        return [False, False, False]

    # H_1: f: G \to H is a group homomorphism
    h1 = False
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        h1 = True
        for a in elements:
            fa = f(a) if callable(f) else f[a]
            
            if hasattr(H, 'contains'):
                if not H.contains(fa):
                    h1 = False
                    break
            else:
                if fa not in H:
                    h1 = False
                    break
                    
            for b in elements:
                ab = a * b
                fab = f(ab) if callable(f) else f[ab]
                fb = f(b) if callable(f) else f[b]
                if fab != fa * fb:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: x is an element of G having finite order
    h2 = False
    try:
        in_G = G.contains(x) if hasattr(G, 'contains') else (x in G)
        if in_G:
            order_x = get_order(x, G)
            if order_x > 0 and order_x != float('inf'):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The order of f(x) in H does NOT divide the order of x in G
    neg_q = False
    try:
        fx = f(x) if callable(f) else f[x]
        order_fx = get_order(fx, H)
        order_x = get_order(x, G)
        
        if order_fx == float('inf'):
            neg_q = True
        elif order_x != float('inf') and order_x > 0 and order_fx > 0:
            if order_x % order_fx != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: x is an element of G having finite order",
    "¬Q: The order of f(x) in H does not divide the order of x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2