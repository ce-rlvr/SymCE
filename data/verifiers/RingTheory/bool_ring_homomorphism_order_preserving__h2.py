import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_boolean_ring(ring):
    elements, add, mul = ring
    if not elements: 
        return False
    
    # Check closure
    for a in elements:
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            
    # Check add commutativity
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
            
    # Check add associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    # Check add identity
    zero = None
    for e in elements:
        if all(add(e, a) == a for a in elements):
            zero = e
            break
    if zero is None: 
        return False
    
    # Check add inverse
    for a in elements:
        if not any(add(a, b) == zero for b in elements): return False
        
    # Check mul associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                
    # Check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    # Check Boolean property (x^2 = x)
    for a in elements:
        if mul(a, a) != a: return False
        
    return True

def conditions(witness):
    """
    witness can be a dictionary:
    {
        'R': (R_elements, R_add, R_mul),
        'S': (S_elements, S_add, S_mul),
        'f': f_mapping,
        'x': x_val,
        'y': y_val
    }
    or a tuple: (R, S, f, x, y)
    """
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            f = witness['f']
            x = witness['x']
            y = witness['y']
        else:
            R, S, f, x, y = witness
    except Exception:
        return [False, False, False, False]

    def extract_ring(ring_obj):
        if hasattr(ring_obj, 'elements') and hasattr(ring_obj, 'add') and hasattr(ring_obj, 'mul'):
            return ring_obj.elements, ring_obj.add, ring_obj.mul
        return ring_obj[0], ring_obj[1], ring_obj[2]

    def get_op(op, elements):
        def apply(a, b):
            if callable(op): return op(a, b)
            if isinstance(op, dict): return op[(a, b)]
            return op[elements.index(a)][elements.index(b)]
        return apply

    def get_f(func):
        def apply(a):
            if callable(func): return func(a)
            if isinstance(func, dict): return func[a]
            return func[a]
        return apply

    # H1: R is a Boolean ring
    try:
        R_elements, R_add_op, R_mul_op = extract_ring(R)
        R_elements = list(R_elements)
        R_add = get_op(R_add_op, R_elements)
        R_mul = get_op(R_mul_op, R_elements)
        h1 = is_boolean_ring((R_elements, R_add, R_mul))
    except Exception:
        h1 = False

    # H2: S is a Boolean ring
    try:
        S_elements, S_add_op, S_mul_op = extract_ring(S)
        S_elements = list(S_elements)
        S_add = get_op(S_add_op, S_elements)
        S_mul = get_op(S_mul_op, S_elements)
        h2 = is_boolean_ring((S_elements, S_add, S_mul))
    except Exception:
        h2 = False

    # H3: x and y are elements of R such that x <= y (i.e., x * y = x)
    try:
        h3 = (x in R_elements) and (y in R_elements) and (R_mul(x, y) == x)
    except Exception:
        h3 = False

    # neg_Q: f(x) <= f(y) in S is FALSE (i.e., f(x) * f(y) != f(x))
    try:
        f_app = get_f(f)
        fx = f_app(x)
        fy = f_app(y)
        
        if fx not in S_elements or fy not in S_elements:
            neg_q = False
        else:
            neg_q = (S_mul(fx, fy) != fx)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: S is a Boolean ring",
    "H_3: x and y are elements of R such that x <= y",
    "¬Q: f(x) <= f(y) in S is false"
]

N_HYP = 3
NEG_Q_INDEX = 3