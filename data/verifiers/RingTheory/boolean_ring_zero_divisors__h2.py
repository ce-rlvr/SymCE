import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with a multiplicative identity 1",
    "H_2: x is a non-zero element of R such that x != 1",
    "¬Q: x is not a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    def _apply(op, a, b):
        if callable(op):
            return op(a, b)
        elif isinstance(op, dict):
            return op[(a, b)]
        else:
            return op[a][b]

    # Extract witness components
    try:
        if isinstance(witness, tuple) and len(witness) >= 6:
            elements, add, mul, zero, one, x = witness[:6]
        elif hasattr(witness, 'elements'):
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            x = witness.x
        elif isinstance(witness, dict):
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            one = witness['one']
            x = witness['x']
        else:
            return [False, False, False]
            
        if callable(elements):
            elements = elements()
        elements = list(elements)
    except Exception:
        return [False, False, False]

    # H_1: R is a Boolean ring with a multiplicative identity 1
    h1_ok = False
    try:
        is_ring = True
        if zero not in elements or one not in elements:
            is_ring = False
        
        if is_ring:
            for a in elements:
                # Identity properties
                if _apply(add, a, zero) != a or _apply(add, zero, a) != a:
                    is_ring = False; break
                if _apply(mul, a, one) != a or _apply(mul, one, a) != a:
                    is_ring = False; break
                # Boolean ring property: x^2 = x
                if _apply(mul, a, a) != a:
                    is_ring = False; break
                
                # Additive inverse
                has_inv = False
                for b in elements:
                    if _apply(add, a, b) == zero and _apply(add, b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    is_ring = False; break

        if is_ring:
            for a, b in itertools.product(elements, repeat=2):
                # Closure
                if _apply(add, a, b) not in elements:
                    is_ring = False; break
                if _apply(mul, a, b) not in elements:
                    is_ring = False; break
                # Commutativity of addition
                if _apply(add, a, b) != _apply(add, b, a):
                    is_ring = False; break

        if is_ring:
            for a, b, c in itertools.product(elements, repeat=3):
                # Associativity
                if _apply(add, a, _apply(add, b, c)) != _apply(add, _apply(add, a, b), c):
                    is_ring = False; break
                if _apply(mul, a, _apply(mul, b, c)) != _apply(mul, _apply(mul, a, b), c):
                    is_ring = False; break
                # Distributivity
                if _apply(mul, a, _apply(add, b, c)) != _apply(add, _apply(mul, a, b), _apply(mul, a, c)):
                    is_ring = False; break
                if _apply(mul, _apply(add, a, b), c) != _apply(add, _apply(mul, a, c), _apply(mul, b, c)):
                    is_ring = False; break
                    
        h1_ok = is_ring
    except Exception:
        h1_ok = False

    # H_2: x is a non-zero element of R such that x != 1
    h2_ok = False
    try:
        if x in elements and x != zero and x != one:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: x is not a zero divisor in R
    neg_q_ok = False
    try:
        is_zero_divisor = False
        if x != zero:
            for y in elements:
                if y != zero:
                    if _apply(mul, x, y) == zero or _apply(mul, y, x) == zero:
                        is_zero_divisor = True
                        break
        neg_q_ok = not is_zero_divisor
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]