import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix
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

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: x and y are conjugate in G",
    "¬Q: The order of x is not equal to the order of y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def in_G(G, x):
    try:
        if hasattr(G, 'contains'):
            if G.contains(x) == True: return True
    except Exception: pass
    try:
        if hasattr(G, 'elements'):
            if any(e == x for e in G.elements): return True
    except Exception: pass
    try:
        count = 0
        for e in G:
            if count > 1000: break
            count += 1
            if e == x: return True
    except Exception: pass
    return False

def is_zero(g):
    try:
        if hasattr(g, 'is_zero_matrix') and g.is_zero_matrix: return True
    except Exception: pass
    try:
        if g == 0: return True
    except Exception: pass
    try:
        if all(e == 0 for e in g): return True
    except Exception: pass
    return False

def are_conjugate(G, x, y, witness):
    # 1. Check if witness explicitly provides conjugating element g
    if isinstance(witness, dict) and 'g' in witness:
        g = witness['g']
        if in_G(G, g) and not is_zero(g):
            try:
                if g * x == y * g: return True
            except Exception: pass
            try:
                if g * x * g**-1 == y: return True
            except Exception: pass
            try:
                if g * x * g.inv() == y: return True
            except Exception: pass
            
    # 2. Check if witness explicitly provides u, v (for semigroup conjugacy x=uv, y=vu)
    if isinstance(witness, dict) and 'u' in witness and 'v' in witness:
        u, v = witness['u'], witness['v']
        if in_G(G, u) and in_G(G, v):
            try:
                if x == u * v and y == v * u: return True
            except Exception: pass

    # 3. Search in G for g
    try:
        count = 0
        for g in G:
            if count > 1000: break
            count += 1
            if is_zero(g): continue
            try:
                if g * x == y * g: return True
            except Exception: pass
            try:
                if g * x * g**-1 == y: return True
            except Exception: pass
            try:
                if g * x * g.inv() == y: return True
            except Exception: pass
    except Exception: pass

    # 4. Search in G for u, v
    try:
        count_u = 0
        for u in G:
            if count_u > 100: break
            count_u += 1
            count_v = 0
            for v in G:
                if count_v > 100: break
                count_v += 1
                try:
                    if x == u * v and y == v * u: return True
                except Exception: pass
    except Exception: pass

    return False

def get_order(x):
    try:
        if hasattr(x, 'order'):
            if callable(x.order):
                return x.order()
            return x.order
    except Exception:
        pass
        
    try:
        if hasattr(x, 'is_Matrix') and x.is_Matrix:
            if x.is_zero_matrix:
                return float('inf')
            I = x.eye(x.rows)
            if x == I: return 1
            curr = x
            for i in range(2, 1000):
                curr = curr * x
                if curr == I: return i
            return float('inf')
    except Exception:
        pass

    try:
        if x == 1: return 1
        curr = x
        for i in range(2, 1000):
            curr = curr * x
            if curr == 1: return i
    except Exception:
        pass
        
    return float('inf')

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        G = witness.get('G')
        x = witness.get('x')
        y = witness.get('y')
    else:
        try:
            G, x, y = witness[:3]
        except Exception:
            return [False, False, False]
            
    try:
        h1 = in_G(G, x) and in_G(G, y)
    except Exception:
        h1 = False
        
    try:
        h2 = are_conjugate(G, x, y, witness)
    except Exception:
        h2 = False
        
    try:
        ox = get_order(x)
        oy = get_order(y)
        neg_q = (ox != oy)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]