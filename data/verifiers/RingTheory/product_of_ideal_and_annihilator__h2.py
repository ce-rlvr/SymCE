import sympy
from sympy import eye, zeros
import itertools

# Top-level setup for common finite rings to help the witness generator
class Zmod:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        
    def add(self, a, b):
        return (a + b) % self.n
        
    def mul(self, a, b):
        return (a * b) % self.n
        
    def __repr__(self):
        return f"Z/{self.n}Z"

Z2 = Zmod(2)
Z3 = Zmod(3)
Z4 = Zmod(4)
Z6 = Zmod(6)
Z8 = Zmod(8)
Z9 = Zmod(9)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Ann(I) is the annihilator ideal of I in R",
    "¬Q: I \\cdot Ann(I) != {0} (or I \\cap Ann(I) != {0})"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(R):
    if hasattr(R, 'elements'):
        return list(R.elements)
    elif hasattr(R, 'ring_elements'):
        return list(R.ring_elements)
    elif isinstance(R, (list, set, tuple)):
        return list(R)
    raise ValueError("Cannot find elements")

def get_ideal_elements(I):
    if hasattr(I, 'elements'):
        return list(I.elements)
    elif isinstance(I, (list, set, tuple)):
        return list(I)
    raise ValueError("Cannot find ideal elements")

def get_add(R):
    if hasattr(R, 'add'):
        return R.add
    return lambda a, b: a + b

def get_mul(R):
    if hasattr(R, 'mul'):
        return R.mul
    return lambda a, b: a * b

def get_zero(R, elements, add_op):
    if hasattr(R, 'zero'):
        return R.zero
    for e in elements:
        if all(add_op(e, x) == x for x in elements) and all(add_op(x, e) == x for x in elements):
            return e
    raise ValueError("No zero found")

def check_commutative_ring(R_elements, add_op, mul_op, zero):
    # check closure
    for a in R_elements:
        for b in R_elements:
            if add_op(a, b) not in R_elements: return False
            if mul_op(a, b) not in R_elements: return False
    
    # check commutativity
    for a in R_elements:
        for b in R_elements:
            if mul_op(a, b) != mul_op(b, a): return False
            if add_op(a, b) != add_op(b, a): return False
            
    # check associativity and distributivity
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                if add_op(add_op(a, b), c) != add_op(a, add_op(b, c)): return False
                if mul_op(mul_op(a, b), c) != mul_op(a, mul_op(b, c)): return False
                if mul_op(a, add_op(b, c)) != add_op(mul_op(a, b), mul_op(a, c)): return False

    # check zero
    for a in R_elements:
        if add_op(a, zero) != a: return False
        
    # check additive inverse
    for a in R_elements:
        has_inv = False
        for b in R_elements:
            if add_op(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    return True

def check_ideal(R_elements, I_elements, add_op, mul_op, zero):
    if not I_elements: return False
    if zero not in I_elements: return False
    
    for a in I_elements:
        for b in I_elements:
            if add_op(a, b) not in I_elements: return False
            
    for r in R_elements:
        for x in I_elements:
            if mul_op(r, x) not in I_elements: return False
            if mul_op(x, r) not in I_elements: return False
            
    return True

def compute_annihilator(R_elements, I_elements, mul_op, zero):
    ann = []
    for r in R_elements:
        if all(mul_op(r, x) == zero for x in I_elements):
            ann.append(r)
    return ann

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            R = witness[0]
            I = witness[1]
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
        else:
            return [False, False, False]
            
        R_elements = get_elements(R)
        add_op = get_add(R)
        mul_op = get_mul(R)
        zero = get_zero(R, R_elements, add_op)
        
        I_elements = get_ideal_elements(I)
        
    except Exception:
        return [False, False, False]

    try:
        h1 = check_commutative_ring(R_elements, add_op, mul_op, zero)
    except Exception:
        h1 = False
        
    try:
        ann_elements = compute_annihilator(R_elements, I_elements, mul_op, zero)
        h2 = check_ideal(R_elements, ann_elements, add_op, mul_op, zero)
        h2 = h2 and check_ideal(R_elements, I_elements, add_op, mul_op, zero)
    except Exception:
        h2 = False
        
    try:
        # The conjecture states I * Ann(I) = {0}. In a commutative ring, this is a tautology.
        # The dropped hypothesis was likely "R is reduced", and the intended conclusion was I \cap Ann(I) = {0}.
        # We check both the intersection and the product to be robust against the typo.
        intersection = [x for x in I_elements if x in ann_elements]
        cap_is_zero = all(x == zero for x in intersection)
        
        prod_is_zero = True
        for i in I_elements:
            for a in ann_elements:
                if mul_op(i, a) != zero:
                    prod_is_zero = False
                    
        neg_q = (not prod_is_zero) or (not cap_is_zero)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]