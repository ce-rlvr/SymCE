import sympy
from sympy import Integer
import itertools
import functools

# Top-level setup: Standard Boolean rings for easy witness construction
Z2_elements = [0, 1]
Z2_add = lambda x, y: (x + y) % 2
Z2_mul = lambda x, y: (x * y) % 2
Z2_zero = 0
Z2_one = 1
Z2_ring = (Z2_elements, Z2_add, Z2_mul, Z2_zero, Z2_one)

Z2xZ2_elements = [(0,0), (0,1), (1,0), (1,1)]
Z2xZ2_add = lambda x, y: ((x[0]+y[0])%2, (x[1]+y[1])%2)
Z2xZ2_mul = lambda x, y: ((x[0]*y[0])%2, (x[1]*y[1])%2)
Z2xZ2_zero = (0,0)
Z2xZ2_one = (1,1)
Z2xZ2_ring = (Z2xZ2_elements, Z2xZ2_add, Z2xZ2_mul, Z2xZ2_zero, Z2xZ2_one)

def get_ring_and_u(witness):
    """
    Parses the witness into (elements, add, mul, zero, one, u).
    Supports passing just an integer (assumes Z_2), a tuple (n, u) for Z_n,
    or a full tuple ((elements, add, mul, zero, one), u).
    """
    if isinstance(witness, (int, Integer)):
        n = 2
        elements = list(range(n))
        add = lambda x, y: (x + y) % n
        mul = lambda x, y: (x * y) % n
        zero = 0
        one = 1
        u = int(witness) % n
        return elements, add, mul, zero, one, u
    
    if isinstance(witness, tuple):
        if len(witness) == 2:
            R_cand, u = witness
            if isinstance(R_cand, (int, Integer)):
                n = int(R_cand)
                elements = list(range(n))
                add = lambda x, y: (x + y) % n
                mul = lambda x, y: (x * y) % n
                zero = 0
                one = 1 % n
                return elements, add, mul, zero, one, u
            elif isinstance(R_cand, tuple) and len(R_cand) == 5:
                elements, add, mul, zero, one = R_cand
                return elements, add, mul, zero, one, u
        elif len(witness) == 6:
            return witness
            
    raise ValueError("Cannot parse witness format")

def check_boolean_ring(elements, add, mul, zero):
    if zero not in elements: 
        return False
    # Limit size to prevent O(N^3) from timing out on invalid large rings
    if len(elements) > 50: 
        return False
        
    for a in elements:
        # Additive identity
        if add(a, zero) != a or add(zero, a) != a: 
            return False
        
        # Additive inverse
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        
        # Boolean property (x^2 = x)
        if mul(a, a) != a: 
            return False
        
        for b in elements:
            # Closure
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            # Commutativity of addition
            if add(a, b) != add(b, a): return False
            
            for c in elements:
                # Associativity
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                # Distributivity
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def check_identity(elements, mul, one):
    if one not in elements: 
        return False
    for a in elements:
        if mul(a, one) != a or mul(one, a) != a: 
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero, one, u = get_ring_and_u(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_boolean_ring(elements, add, mul, zero)
    except Exception:
        h1 = False
        
    try:
        h2 = check_identity(elements, mul, one)
    except Exception:
        h2 = False
        
    try:
        neg_q = (u != one) and (u in elements)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has a multiplicative identity 1",
    "¬Q: u != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2