import sympy
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class CustomRing:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self._add = add_func
        self._mul = mul_func
        self.zero = zero

    def add(self, x, y):
        return self._add(x, y)

    def mul(self, x, y):
        return self._mul(x, y)

def ZeroRing(n):
    """Returns a ring with n elements where all products are zero."""
    elements = list(range(n))
    def add(x, y): return (x + y) % n
    def mul(x, y): return 0
    return CustomRing(elements, add, mul, 0)

def Z(n):
    """Returns the ring of integers modulo n."""
    elements = list(range(n))
    def add(x, y): return (x + y) % n
    def mul(x, y): return (x * y) % n
    return CustomRing(elements, add, mul, 0)

def additive_closure(R, subset):
    closure = set([R.zero])
    closure.update(subset)
    added = True
    while added:
        added = False
        new_elements = set()
        for x in closure:
            for y in closure:
                s = R.add(x, y)
                if s not in closure and s not in new_elements:
                    new_elements.add(s)
        if new_elements:
            closure.update(new_elements)
            added = True
    return frozenset(closure)

def left_ideal_generated_by(R, subset):
    generators = set(subset)
    for s in subset:
        for r in R.elements:
            generators.add(R.mul(r, s))
    return additive_closure(R, generators)

def get_all_left_ideals(R):
    principal_ideals = set()
    for x in R.elements:
        principal_ideals.add(left_ideal_generated_by(R, [x]))
    
    ideals = set(principal_ideals)
    added = True
    while added:
        added = False
        new_ideals = set()
        for I in ideals:
            for J in principal_ideals:
                sum_ideal = set()
                for i in I:
                    for j in J:
                        sum_ideal.add(R.add(i, j))
                sum_ideal = frozenset(sum_ideal)
                if sum_ideal not in ideals and sum_ideal not in new_ideals:
                    new_ideals.add(sum_ideal)
        if new_ideals:
            ideals.update(new_ideals)
            added = True
    return ideals

def is_semisimple(R):
    ideals = get_all_left_ideals(R)
    R_set = frozenset(R.elements)
    zero_set = frozenset([R.zero])
    
    for I in ideals:
        has_complement = False
        for J in ideals:
            if I.intersection(J) == zero_set:
                sum_IJ = set()
                for i in I:
                    for j in J:
                        sum_IJ.add(R.add(i, j))
                if frozenset(sum_IJ) == R_set:
                    has_complement = True
                    break
        if not has_complement:
            return False
    return True

def has_identity(R):
    for e in R.elements:
        is_id = True
        for x in R.elements:
            if R.mul(e, x) != x or R.mul(x, e) != x:
                is_id = False
                break
        if is_id:
            return True
    return False

def is_left_artinian(R):
    return len(R.elements) >= 1

def is_product_of_matrix_rings(R):
    # A finite ring is isomorphic to a finite direct product of matrix rings 
    # over division rings if and only if it is semisimple and has a multiplicative identity.
    return is_semisimple(R) and has_identity(R)

CONDITION_LABELS = [
    "H_1: R is a left Artinian ring",
    "H_2: R is a semisimple ring",
    "¬Q: R is not isomorphic to a finite direct product of matrix rings over division rings"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        h1 = is_left_artinian(witness)
    except Exception:
        h1 = False

    try:
        h2 = is_semisimple(witness)
    except Exception:
        h2 = False

    try:
        q = is_product_of_matrix_rings(witness)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]