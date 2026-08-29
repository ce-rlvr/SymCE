import itertools
import math
from sympy import eye, zeros

# Standard algebra objects that might be used to construct a witness
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Helper for a simple Z2 Boolean ring
Z2_elements = [0, 1]
def Z2_add(a, b): return (a + b) % 2
def Z2_mul(a, b): return (a * b) % 2

def evaluate_op(op, a, b, elements):
    if callable(op):
        return op(a, b)
    elif isinstance(op, dict):
        return op[(a, b)]
    elif isinstance(op, (list, tuple)):
        idx_a = elements.index(a)
        idx_b = elements.index(b)
        return op[idx_a][idx_b]
    else:
        raise ValueError("Unknown operator format")

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: (elements, add, mul, x, y) or (elements, add, mul, leq, x, y)
    """
    try:
        if len(witness) == 6:
            elements, add, mul, leq, x, y = witness
        elif len(witness) == 5:
            elements, add, mul, x, y = witness
            leq = lambda a, b: evaluate_op(mul, a, b, elements) == a
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def add_op(a, b): return evaluate_op(add, a, b, elements)
    def mul_op(a, b): return evaluate_op(mul, a, b, elements)
    def leq_op(a, b): return evaluate_op(leq, a, b, elements)

    # H_1: R is a Boolean ring
    h1_ok = False
    try:
        if not isinstance(elements, (list, tuple)) or len(elements) == 0:
            raise ValueError
        if x not in elements or y not in elements:
            raise ValueError
            
        # Check closure
        for a in elements:
            for b in elements:
                if add_op(a, b) not in elements: raise ValueError
                if mul_op(a, b) not in elements: raise ValueError
                
        # Check commutativity of add
        for a in elements:
            for b in elements:
                if add_op(a, b) != add_op(b, a): raise ValueError
                
        # Check associativity and distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if add_op(add_op(a, b), c) != add_op(a, add_op(b, c)): raise ValueError
                    if mul_op(mul_op(a, b), c) != mul_op(a, mul_op(b, c)): raise ValueError
                    if mul_op(a, add_op(b, c)) != add_op(mul_op(a, b), mul_op(a, c)): raise ValueError
                    if mul_op(add_op(a, b), c) != add_op(mul_op(a, c), mul_op(b, c)): raise ValueError
                    
        # Check additive identity
        zeros_list = []
        for z in elements:
            if all(add_op(z, a) == a and add_op(a, z) == a for a in elements):
                zeros_list.append(z)
        if not zeros_list: raise ValueError
        zero = zeros_list[0]
        
        # Check additive inverses
        for a in elements:
            if not any(add_op(a, b) == zero and add_op(b, a) == zero for b in elements):
                raise ValueError
                
        # Check Boolean condition (x^2 = x)
        for a in elements:
            if mul_op(a, a) != a: raise ValueError
            
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: <= is the partial order defined by a <= b iff ab = a
    h2_ok = False
    try:
        valid = True
        for a in elements:
            for b in elements:
                if bool(leq_op(a, b)) != (mul_op(a, b) == a):
                    valid = False
                    break
            if not valid: break
        h2_ok = valid
    except Exception:
        h2_ok = False

    # neg_Q: x+y is NOT the supremum of x and y with respect to <=
    neg_q_ok = False
    try:
        s = add_op(x, y)
        
        # Check if s is an upper bound
        is_upper_bound = bool(leq_op(x, s)) and bool(leq_op(y, s))
        
        is_least_upper_bound = False
        if is_upper_bound:
            is_least_upper_bound = True
            # Check if it is the least upper bound
            for z in elements:
                if bool(leq_op(x, z)) and bool(leq_op(y, z)):
                    # z is an upper bound, so s must be <= z
                    if not bool(leq_op(s, z)):
                        is_least_upper_bound = False
                        break
                        
        neg_q_ok = not is_least_upper_bound
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: <= is the partial order defined by a <= b iff ab = a",
    "¬Q: x+y is not the supremum of x and y with respect to <="
]

N_HYP = 2
NEG_Q_INDEX = 2