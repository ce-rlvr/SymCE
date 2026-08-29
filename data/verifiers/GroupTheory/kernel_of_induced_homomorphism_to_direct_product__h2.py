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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def evaluate(func, x):
    if isinstance(func, dict):
        return func[x]
    elif callable(func):
        return func(x)
    else:
        raise ValueError("Function must be a dict or callable")

def check_g(G, H2, g):
    elements = get_elements(G)
    H2_elements = get_elements(H2)
    for x in elements:
        gx = evaluate(g, x)
        if gx not in H2_elements:
            return False
    for x in elements:
        for y in elements:
            gxy = evaluate(g, x * y)
            gx = evaluate(g, x)
            gy = evaluate(g, y)
            if gxy != gx * gy:
                return False
    return True

def check_f(G, H1, f):
    elements = get_elements(G)
    H1_elements = get_elements(H1)
    for x in elements:
        fx = evaluate(f, x)
        if fx not in H1_elements:
            return False
    return True

def check_neg_q(G, f, g):
    elements = get_elements(G)
    for x in elements:
        for y in elements:
            fxy = evaluate(f, x * y)
            fx = evaluate(f, x)
            fy = evaluate(f, y)
            
            gxy = evaluate(g, x * y)
            gx = evaluate(g, x)
            gy = evaluate(g, y)
            
            if fxy != fx * fy or gxy != gx * gy:
                return True
    return False

def conditions(witness):
    try:
        G = witness['G']
        H1 = witness['H1']
        H2 = witness['H2']
        f = witness['f']
        g = witness['g']
    except Exception:
        return [False, False, False, False]
        
    try:
        h1_ok = hasattr(G, 'elements') and hasattr(H1, 'elements') and hasattr(H2, 'elements')
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = check_g(G, H2, g)
    except Exception:
        h2_ok = False
        
    try:
        h3_ok = check_f(G, H1, f)
    except Exception:
        h3_ok = False
        
    try:
        neg_q = check_neg_q(G, f, g)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G, H_1, and H_2 are groups",
    "H_2: g is a group homomorphism from G to H_2",
    "H_3: f is a function from G to H_1",
    "¬Q: \phi is not a group homomorphism (so it has no kernel)"
]

N_HYP = 3
NEG_Q_INDEX = 3