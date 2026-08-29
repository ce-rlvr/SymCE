import itertools

class Z2Ring:
    elements = [0, 1]
    zero = 0
    @staticmethod
    def add(x, y): return (x + y) % 2
    @staticmethod
    def mul(x, y): return (x * y) % 2

class Z2xZ2Ring:
    elements = [(0,0), (0,1), (1,0), (1,1)]
    zero = (0,0)
    @staticmethod
    def add(x, y): return ((x[0]+y[0])%2, (x[1]+y[1])%2)
    @staticmethod
    def mul(x, y): return ((x[0]*y[0])%2, (x[1]*y[1])%2)

Z2 = Z2Ring()
Z2xZ2 = Z2xZ2Ring()

def get_ring_ops(witness):
    w_a = getattr(witness, 'a', None)
    w_b = getattr(witness, 'b', None)
    
    if hasattr(witness, 'ring'):
        R = witness.ring
    elif isinstance(witness, tuple) and len(witness) == 3 and hasattr(witness[0], 'elements'):
        R, w_a, w_b = witness
    else:
        R = witness

    if hasattr(R, 'elements'):
        elements = list(R.elements)
    else:
        elements = list(R)
        
    if hasattr(R, 'add'):
        add = R.add
    else:
        add = lambda x, y: x + y
        
    if hasattr(R, 'mul'):
        mul = R.mul
    else:
        mul = lambda x, y: x * y
        
    if hasattr(R, 'zero'):
        zero = R.zero
    else:
        zero = elements[0]
        for e in elements:
            if all(add(e, x) == x for x in elements):
                zero = e
                break
                
    return elements, add, mul, zero, w_a, w_b

def is_gcd(g, a, b, elements, add, mul):
    # Check if g divides a (i.e., exists x such that a = g * x)
    if not any(a == mul(g, x) for x in elements):
        return False
        
    # Check if g divides b
    if not any(b == mul(g, x) for x in elements):
        return False
        
    # Check if for all c, if c divides a and c divides b, then c divides g
    for c in elements:
        c_div_a = any(a == mul(c, x) for x in elements)
        c_div_b = any(b == mul(c, x) for x in elements)
        if c_div_a and c_div_b:
            c_div_g = any(g == mul(c, x) for x in elements)
            if not c_div_g:
                return False
                
    return True

def conditions(witness):
    try:
        elements, add, mul, zero, w_a, w_b = get_ring_ops(witness)
    except Exception:
        return [False, False]
        
    # H_1: R is a Boolean ring
    is_boolean_ring = True
    try:
        # Check the defining property of a Boolean ring: x^2 = x for all x
        for x in elements:
            if mul(x, x) != x:
                is_boolean_ring = False
                break
    except Exception:
        is_boolean_ring = False
        
    # ¬Q: The element a + b + ab is NOT a greatest common divisor of a and b in R
    try:
        conclusion_holds = True
        pairs = [(w_a, w_b)] if w_a is not None and w_b is not None else [(a, b) for a in elements for b in elements]
        
        for a_val, b_val in pairs:
            ab = mul(a_val, b_val)
            a_plus_b = add(a_val, b_val)
            g = add(a_plus_b, ab)
            
            if not is_gcd(g, a_val, b_val, elements, add, mul):
                conclusion_holds = False
                break
                
        neg_Q = not conclusion_holds
    except Exception:
        neg_Q = False
        
    return [is_boolean_ring, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The element a + b + ab is not a greatest common divisor of a and b in R"
]

N_HYP = 1
NEG_Q_INDEX = 1