import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
import itertools
import math
import functools

# Top-level setup for potential witness references
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to be an object representing a ring with the following attributes:
      - elements: an iterable of the ring's elements
      - add: a function(a, b) returning the sum a + b
      - mul: a function(a, b) returning the product ab
      - zero: the additive identity element
      - x: an element of the ring
      - y: an element of the ring
      - leq: (optional) a function(a, b) returning True if a <= b. Defaults to ab == a.
    """
    try:
        elements = list(witness.elements)
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        x = witness.x
        y = witness.y
    except Exception:
        return [False, False, False]
        
    # H1: R is a Boolean ring
    # A Boolean ring is a ring where a^2 = a for all a in R.
    h1 = True
    try:
        if zero not in elements:
            h1 = False
        else:
            for a in elements:
                if not h1: break
                
                # Zero identity
                if add(a, zero) != a or add(zero, a) != a:
                    h1 = False
                    break
                
                # Idempotence (Boolean ring property)
                if mul(a, a) != a:
                    h1 = False
                    break
                
                # Additive inverse
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                
                # Ring axioms: closure, associativity, commutativity of addition, distributivity
                for b in elements:
                    if not h1: break
                    if add(a, b) not in elements:
                        h1 = False
                        break
                    if mul(a, b) not in elements:
                        h1 = False
                        break
                    if add(a, b) != add(b, a):
                        h1 = False
                        break
                    
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)):
                            h1 = False
                            break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)):
                            h1 = False
                            break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                            h1 = False
                            break
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                            h1 = False
                            break
    except Exception:
        h1 = False

    # H2: x and y are elements of R such that xy = 0
    h2 = True
    try:
        if x not in elements or y not in elements:
            h2 = False
        elif mul(x, y) != zero:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The sum x+y is NOT the least upper bound (supremum) of x and y with respect to <=
    neg_q = False
    try:
        def leq(a, b):
            if hasattr(witness, 'leq'):
                return witness.leq(a, b)
            return mul(a, b) == a
            
        s = add(x, y)
        
        # Check if s is an upper bound
        is_ub = leq(x, s) and leq(y, s)
        
        if not is_ub:
            neg_q = True
        else:
            # Check if s is the LEAST upper bound
            is_least = True
            for z in elements:
                if leq(x, z) and leq(y, z):
                    if not leq(s, z):
                        is_least = False
                        break
            if not is_least:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: x and y are elements of R such that xy = 0",
    "¬Q: The sum x+y is NOT the least upper bound (supremum) of x and y with respect to the partial order <="
]

N_HYP = 2
NEG_Q_INDEX = 2