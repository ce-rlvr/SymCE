import itertools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_set(X):
    for i in range(len(X)):
        for j in range(i+1, len(X)):
            if X[i] == X[j]: 
                return False
    return True

def is_boolean_ring(elements, add, mul):
    if not elements: 
        return False
    elements = list(elements)
    
    # check closure
    for a in elements:
        for b in elements:
            try:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
            except Exception:
                return False
                
    # check commutativity of add
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
            
    # check associativity of add
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    # find zero
    zeros_list = []
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zeros_list.append(z)
    if not zeros_list: 
        return False
    zero = zeros_list[0]
    
    # check inverses
    for a in elements:
        if not any(add(a, b) == zero for b in elements): return False
        
    # check associativity of mul
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                
    # check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    # check boolean property
    for a in elements:
        if mul(a, a) != a: return False
        
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            X = witness['X']
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            RX = witness.get('RX', None)
            rx_add = witness.get('rx_add', None)
            rx_mul = witness.get('rx_mul', None)
        elif hasattr(witness, 'X'):
            X = witness.X
            R = witness.R
            add = witness.add
            mul = witness.mul
            RX = getattr(witness, 'RX', None)
            rx_add = getattr(witness, 'rx_add', None)
            rx_mul = getattr(witness, 'rx_mul', None)
        else:
            X = witness[0]
            R = witness[1]
            add = witness[2]
            mul = witness[3]
            if len(witness) >= 7:
                RX = witness[4]
                rx_add = witness[5]
                rx_mul = witness[6]
            else:
                RX = rx_add = rx_mul = None
    except Exception:
        return [False, False, False, False]

    # H1: X is a non-empty set
    try:
        h1 = len(X) > 0 and is_set(X)
    except Exception:
        h1 = False

    # H2: R is a Boolean ring
    try:
        h2 = is_boolean_ring(R, add, mul)
    except Exception:
        h2 = False

    # H3: Define addition and multiplication on R^X pointwise
    try:
        if RX is None:
            RX_constructed = list(itertools.product(R, repeat=len(X)))
            def rx_add_constructed(f, g):
                return tuple(add(f[i], g[i]) for i in range(len(X)))
            def rx_mul_constructed(f, g):
                return tuple(mul(f[i], g[i]) for i in range(len(X)))
            RX = RX_constructed
            rx_add = rx_add_constructed
            rx_mul = rx_mul_constructed
            h3 = True
        else:
            RX_constructed = list(itertools.product(R, repeat=len(X)))
            if len(RX) != len(RX_constructed):
                h3 = False
            else:
                h3 = True
                for f in RX:
                    for g in RX:
                        if rx_add(f, g) != tuple(add(f[i], g[i]) for i in range(len(X))):
                            h3 = False
                        if rx_mul(f, g) != tuple(mul(f[i], g[i]) for i in range(len(X))):
                            h3 = False
    except Exception:
        h3 = False

    # neg_Q: R^X is not a Boolean ring
    try:
        neg_q = not is_boolean_ring(RX, rx_add, rx_mul)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: R is a Boolean ring",
    "H_3: Addition and multiplication on R^X are defined pointwise",
    "¬Q: R^X is not a Boolean ring"
]

N_HYP = 3
NEG_Q_INDEX = 3