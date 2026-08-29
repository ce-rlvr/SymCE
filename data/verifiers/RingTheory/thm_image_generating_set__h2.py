import itertools

class FiniteRing:
    def __init__(self, elements, add, mul, neg, zero):
        self.elements = list(elements)
        self.add = add
        self.mul = mul
        self.neg = neg
        self.zero = zero

def Z(n):
    return FiniteRing(
        elements=list(range(n)),
        add=lambda a, b: (a + b) % n,
        mul=lambda a, b: (a * b) % n,
        neg=lambda a: (-a) % n,
        zero=0
    )

Z2 = Z(2)
Z3 = Z(3)
Z4 = Z(4)
Z5 = Z(5)
Z6 = Z(6)

def ProductRing(R1, R2):
    elements = list(itertools.product(R1.elements, R2.elements))
    return FiniteRing(
        elements=elements,
        add=lambda a, b: (R1.add(a[0], b[0]), R2.add(a[1], b[1])),
        mul=lambda a, b: (R1.mul(a[0], b[0]), R2.mul(a[1], b[1])),
        neg=lambda a: (R1.neg(a[0]), R2.neg(a[1])),
        zero=(R1.zero, R2.zero)
    )

def get_attr(obj, attr):
    if isinstance(obj, dict):
        return obj[attr]
    return getattr(obj, attr)

def is_ring(ring):
    try:
        elements = get_attr(ring, 'elements')
        add = get_attr(ring, 'add')
        mul = get_attr(ring, 'mul')
        neg = get_attr(ring, 'neg')
        zero = get_attr(ring, 'zero')
        
        if zero not in elements: 
            return False
        
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: 
                return False
            if add(a, neg(a)) != zero or add(neg(a), a) != zero: 
                return False
            for b in elements:
                if add(a, b) not in elements: 
                    return False
                if mul(a, b) not in elements: 
                    return False
                if add(a, b) != add(b, a): 
                    return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): 
                        return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): 
                        return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): 
                        return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): 
                        return False
        return True
    except Exception:
        return False

def generates_ring(X, ring):
    try:
        elements = get_attr(ring, 'elements')
        add = get_attr(ring, 'add')
        mul = get_attr(ring, 'mul')
        neg = get_attr(ring, 'neg')
        zero = get_attr(ring, 'zero')
        
        def get_closure(initial_set):
            closure = set(initial_set)
            if not closure:
                closure.add(zero)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for a in closure:
                    if neg(a) not in closure:
                        new_elements.add(neg(a))
                    for b in closure:
                        if add(a, b) not in closure:
                            new_elements.add(add(a, b))
                        if mul(a, b) not in closure:
                            new_elements.add(mul(a, b))
                if new_elements:
                    closure.update(new_elements)
                    changed = True
            return closure

        # Check non-unital closure
        if get_closure(X) == set(elements):
            return True
            
        # Check unital closure (if the ring has a multiplicative identity)
        ones = [e for e in elements if all(mul(e, a) == a and mul(a, e) == a for a in elements)]
        if ones:
            unital_initial = set(X)
            unital_initial.add(ones[0])
            if get_closure(unital_initial) == set(elements):
                return True
                
        return False
    except Exception:
        return False

def get_image(f, X):
    if isinstance(f, dict):
        return [f[x] for x in X]
    elif callable(f):
        return [f(x) for x in X]
    else:
        raise ValueError("f must be a dict or callable")

def conditions(witness):
    """
    witness is expected to be a dictionary with keys:
      'R': FiniteRing or dict representing the domain ring
      'S': FiniteRing or dict representing the codomain ring
      'X': list or set of elements in R
      'f': dict or callable representing the mapping from R to S
    """
    try:
        R = witness['R']
        S = witness['S']
        X = witness['X']
        f = witness['f']
    except Exception:
        return [False, False, False]
        
    # H_1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False
        
    # H_2: X is a subset of R that generates R as a ring
    try:
        R_elements = get_attr(R, 'elements')
        h2 = set(X).issubset(set(R_elements)) and generates_ring(X, R)
    except Exception:
        h2 = False
        
    # ¬Q: The image f(X) does NOT generate S as a ring
    try:
        S_elements = get_attr(S, 'elements')
        f_R = get_image(f, R_elements)
        
        # f must be a valid function from R to S
        if not set(f_R).issubset(set(S_elements)):
            neg_q = False
        else:
            f_X = get_image(f, X)
            neg_q = not generates_ring(f_X, S)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: X is a subset of R that generates R as a ring",
    "¬Q: The image f(X) does not generate S as a ring"
]

N_HYP = 2
NEG_Q_INDEX = 2