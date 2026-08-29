import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness elements
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_witness(witness):
    """
    Extracts the ring elements, addition, multiplication, and optionally a and b.
    Supports tuples, dicts, and objects with attributes.
    """
    a = None
    b = None
    if isinstance(witness, tuple):
        if len(witness) >= 5:
            elements, add_op, mul_op, a, b = witness[:5]
        elif len(witness) >= 3:
            elements, add_op, mul_op = witness[:3]
            if len(witness) == 4:
                a = witness[3]
        else:
            raise ValueError("Witness tuple too short")
    elif isinstance(witness, dict):
        elements = witness['elements']
        add_op = witness['add']
        mul_op = witness['mul']
        a = witness.get('a')
        b = witness.get('b')
    else:
        elements = witness.elements
        add_op = witness.add
        mul_op = witness.mul
        a = getattr(witness, 'a', None)
        b = getattr(witness, 'b', None)
        
    elements_list = []
    for i, e in enumerate(elements):
        if i > 100:  # Prevent infinite or overly large rings from hanging
            raise ValueError("Ring too large")
        elements_list.append(e)
        
    def make_func(op):
        if callable(op): return op
        if isinstance(op, dict): return lambda x, y: op[(x, y)]
        return lambda x, y: op[x][y]
        
    return elements_list, make_func(add_op), make_func(mul_op), a, b

def is_boolean_ring(elements, add, mul):
    n = len(elements)
    if n == 0: return False
    
    # Check closure
    for x in elements:
        for y in elements:
            try:
                if add(x, y) not in elements: return False
                if mul(x, y) not in elements: return False
            except Exception:
                return False
                
    # Check add commutativity and associativity
    for x in elements:
        for y in elements:
            if add(x, y) != add(y, x): return False
            for z in elements:
                if add(x, add(y, z)) != add(add(x, y), z): return False
                
    # Find zero
    zeros_list = []
    for z in elements:
        if all(add(x, z) == x for x in elements):
            zeros_list.append(z)
    if not zeros_list: return False
    zero = zeros_list[0]
    
    # Check additive inverses
    for x in elements:
        if not any(add(x, y) == zero for y in elements): return False
        
    # Check mul associativity
    for x in elements:
        for y in elements:
            for z in elements:
                if mul(x, mul(y, z)) != mul(mul(x, y), z): return False
                
    # Check distributivity
    for x in elements:
        for y in elements:
            for z in elements:
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                if mul(add(y, z), x) != add(mul(y, x), mul(z, x)): return False
                
    # Check Boolean property (x^2 = x)
    for x in elements:
        if mul(x, x) != x: return False
        
    return True

def check_neg_Q(elements, add, mul, a, b):
    def divides(x, y):
        # x divides y if there exists c such that y = x*c or y = c*x
        return any(mul(x, c) == y or mul(c, x) == y for c in elements)
        
    if a is not None and b is not None:
        if a not in elements or b not in elements:
            return False
        ab_eq_b = (mul(a, b) == b)
        return divides(a, b) != ab_eq_b
    else:
        # If specific elements a, b are not provided, search for a counterexample pair
        for x in elements:
            for y in elements:
                if divides(x, y) != (mul(x, y) == y):
                    return True
        return False

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, a, b = extract_witness(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_boolean_ring(elements, add, mul)
    except Exception:
        h1 = False
        
    try:
        neg_q = check_neg_Q(elements, add, mul, a, b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: a divides b is not equivalent to ab = b"
]

N_HYP = 1
NEG_Q_INDEX = 1