import itertools

class FiniteRing:
    def __init__(self, elements, add_func, mul_func):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func

Z2 = FiniteRing(
    [0, 1],
    lambda x, y: (x + y) % 2,
    lambda x, y: (x * y) % 2
)

Z2xZ2 = FiniteRing(
    [(0,0), (0,1), (1,0), (1,1)],
    lambda x, y: ((x[0] + y[0]) % 2, (x[1] + y[1]) % 2),
    lambda x, y: ((x[0] * y[0]) % 2, (x[1] * y[1]) % 2)
)

Z2xZ2xZ2 = FiniteRing(
    list(itertools.product([0,1], repeat=3)),
    lambda x, y: ((x[0] + y[0]) % 2, (x[1] + y[1]) % 2, (x[2] + y[2]) % 2),
    lambda x, y: ((x[0] * y[0]) % 2, (x[1] * y[1]) % 2, (x[2] * y[2]) % 2)
)

def get_elements(R):
    elements = []
    for i, e in enumerate(R.elements):
        if i > 50:
            return None
        if e not in elements:
            elements.append(e)
    return elements

def is_ring(R):
    try:
        elements = get_elements(R)
        if elements is None: return False
        add = R.add
        mul = R.mul
        
        # Check closure
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                
        # Check addition associativity
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    
        # Check addition commutativity
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
                
        # Check additive identity
        zero = None
        for e in elements:
            if all(add(e, a) == a for a in elements):
                zero = e
                break
        if zero is None: return False
        
        # Check additive inverse
        for a in elements:
            if not any(add(a, b) == zero for b in elements): return False
            
        # Check multiplication associativity
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
                    
        return True
    except Exception:
        return False

def is_boolean_ring(R):
    if not is_ring(R): return False
    try:
        elements = get_elements(R)
        mul = R.mul
        for a in elements:
            if mul(a, a) != a: return False
        return True
    except Exception:
        return False

def has_multiplicative_identity(R):
    try:
        elements = get_elements(R)
        if elements is None: return False
        mul = R.mul
        for e in elements:
            if all(mul(e, a) == a and mul(a, e) == a for a in elements):
                return True
        return False
    except Exception:
        return False

def is_isomorphic_to_Z2(R):
    try:
        elements = get_elements(R)
        if elements is None or len(elements) != 2:
            return False
        
        zeros = [e for e in elements if all(R.add(e, a) == a for a in elements)]
        if not zeros:
            return False
        zero = zeros[0]
        one = [e for e in elements if e != zero][0]
        
        # Check Z2 addition table
        if R.add(zero, zero) != zero: return False
        if R.add(zero, one) != one: return False
        if R.add(one, zero) != one: return False
        if R.add(one, one) != zero: return False
        
        # Check Z2 multiplication table
        if R.mul(zero, zero) != zero: return False
        if R.mul(zero, one) != zero: return False
        if R.mul(one, zero) != zero: return False
        if R.mul(one, one) != one: return False
        
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_boolean_ring(witness)
    except Exception:
        h1 = False

    try:
        h2 = has_multiplicative_identity(witness)
    except Exception:
        h2 = False

    try:
        neg_q = not is_isomorphic_to_Z2(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has a multiplicative identity",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2