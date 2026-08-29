import operator
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def parse_witness(witness):
    Z_R = None
    if isinstance(witness, dict):
        elements = witness.get('elements')
        if elements is None and 'n' in witness:
            elements = list(range(witness['n']))
        add = witness.get('add', operator.add)
        mult = witness.get('mult', operator.mul)
        I = witness.get('I', [])
        Z_R = witness.get('Z_R', None)
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            elements, add, mult, I = witness
            if isinstance(elements, int):
                elements = list(range(elements))
        elif len(witness) == 5:
            elements, add, mult, I, Z_R = witness
            if isinstance(elements, int):
                elements = list(range(elements))
        elif len(witness) == 2:
            elements, I = witness
            add, mult = operator.add, operator.mul
        else:
            raise ValueError("Tuple witness must have length 2, 4, or 5")
    else:
        elements = witness.elements
        add = getattr(witness, 'add', operator.add)
        mult = getattr(witness, 'mult', operator.mul)
        I = witness.I
        Z_R = getattr(witness, 'Z_R', None)

    if isinstance(add, list):
        add_f = lambda x, y: add[elements.index(x)][elements.index(y)]
    elif isinstance(add, dict):
        add_f = lambda x, y: add[(x, y)]
    else:
        add_f = add

    if isinstance(mult, list):
        mult_f = lambda x, y: mult[elements.index(x)][elements.index(y)]
    elif isinstance(mult, dict):
        mult_f = lambda x, y: mult[(x, y)]
    else:
        mult_f = mult
        
    return elements, add_f, mult_f, I, Z_R

def check_ring(elements, add_f, mult_f):
    n = len(elements)
    if n == 0: return False
    
    zero = None
    for a in elements:
        is_zero = True
        for b in elements:
            s = add_f(a, b)
            if s not in elements: return False
            if s != b: is_zero = False
            s2 = add_f(b, a)
            if s2 != s: return False
        if is_zero:
            zero = a
            
    if zero is None:
        return False
        
    for a in elements:
        has_inv = False
        for b in elements:
            if add_f(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            for c in elements:
                if add_f(add_f(a, b), c) != add_f(a, add_f(b, c)):
                    return False
                    
    for a in elements:
        for b in elements:
            p = mult_f(a, b)
            if p not in elements: return False
                
            for c in elements:
                if mult_f(mult_f(a, b), c) != mult_f(a, mult_f(b, c)):
                    return False
                if mult_f(a, add_f(b, c)) != add_f(mult_f(a, b), mult_f(a, c)):
                    return False
                if mult_f(add_f(a, b), c) != add_f(mult_f(a, c), mult_f(b, c)):
                    return False
                    
    return True

def check_ideal(elements, add_f, mult_f, I):
    if not I: return False
    for i in I:
        if i not in elements: return False
        
    zero = None
    for a in elements:
        if all(add_f(a, b) == b for b in elements):
            zero = a
            break
    if zero not in I: return False
    
    for i in I:
        for j in I:
            if add_f(i, j) not in I: return False
            
    for i in I:
        has_inv = False
        for j in I:
            if add_f(i, j) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for i in I:
        for r in elements:
            if mult_f(i, r) not in I: return False
            if mult_f(r, i) not in I: return False
            
    return True

def get_center(elements, mult_f):
    center = []
    for a in elements:
        is_center = True
        for b in elements:
            if mult_f(a, b) != mult_f(b, a):
                is_center = False
                break
        if is_center:
            center.append(a)
    return center

def is_equiv(a, b, elements, add_f, I):
    zero = None
    for x in elements:
        if all(add_f(x, y) == y for y in elements):
            zero = x
            break
    inv_b = None
    for x in elements:
        if add_f(b, x) == zero:
            inv_b = x
            break
    return add_f(a, inv_b) in I

def check_neg_Q(elements, add_f, mult_f, I, Z_R):
    for z in Z_R:
        for r in elements:
            zr = mult_f(z, r)
            rz = mult_f(r, z)
            if not is_equiv(zr, rz, elements, add_f, I):
                return True
    return False

def conditions(witness):
    try:
        elements, add_f, mult_f, I, Z_R = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_ring(elements, add_f, mult_f)
    except Exception:
        h1 = False
        
    try:
        h2 = check_ideal(elements, add_f, mult_f, I)
    except Exception:
        h2 = False
        
    try:
        computed_center = get_center(elements, mult_f)
        if Z_R is not None:
            h3 = sorted([elements.index(x) for x in Z_R]) == sorted([elements.index(x) for x in computed_center])
        else:
            Z_R = computed_center
            h3 = True
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(elements, add_f, mult_f, I, Z_R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: Z(R) is the center of R",
    "¬Q: The image \\pi(Z(R)) is not contained in the center of R/I"
]

N_HYP = 3
NEG_Q_INDEX = 3