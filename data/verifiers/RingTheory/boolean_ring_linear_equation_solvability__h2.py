import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer

# Standard named objects
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

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (R, a, b) where R is a Boolean ring, 
    and a, b are elements (potentially from an overring) that violate the conclusion.
    """
    try:
        R, a, b = witness
    except Exception:
        return [False, False]
    
    def is_eq(x, y):
        try:
            return bool(x == y)
        except Exception:
            return False

    def contains(lst, item):
        return any(is_eq(x, item) for x in lst)

    # H_1: R is a Boolean ring
    def is_boolean_ring(ring_elements):
        try:
            elements = list(ring_elements)
            if not elements: 
                return False
            
            # Find the additive identity (zero)
            zero = None
            for z in elements:
                if all(is_eq(z + x, x) for x in elements) and all(is_eq(x + z, x) for x in elements):
                    zero = z
                    break
            if zero is None: 
                return False
            
            # Check ring axioms and Boolean ring property (x^2 = x)
            for x in elements:
                if not is_eq(x * x, x): 
                    return False
                if not any(is_eq(x + y, zero) for y in elements): 
                    return False
                for y in elements:
                    if not contains(elements, x + y): 
                        return False
                    if not contains(elements, x * y): 
                        return False
                    if not is_eq(x + y, y + x): 
                        return False
                    for z in elements:
                        if not is_eq((x + y) + z, x + (y + z)): 
                            return False
                        if not is_eq((x * y) * z, x * (y * z)): 
                            return False
                        if not is_eq(x * (y + z), (x * y) + (x * z)): 
                            return False
                        if not is_eq((x + y) * z, (x * z) + (y * z)): 
                            return False
            return True
        except Exception:
            return False

    try:
        h1_ok = is_boolean_ring(R)
    except Exception:
        h1_ok = False

    # neg_Q: The equation ax = b has a solution for x in R if and only if ab = b (must FAIL)
    try:
        def check_solution(x):
            try:
                return is_eq(a * x, b)
            except Exception:
                return False
                
        has_solution = any(check_solution(x) for x in R)
        
        try:
            ab_equals_b = is_eq(a * b, b)
        except Exception:
            ab_equals_b = False
            
        # The conclusion fails if the equivalence does not hold
        neg_q_ok = (has_solution != ab_equals_b)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The equivalence (ax = b has a solution in R iff ab = b) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1