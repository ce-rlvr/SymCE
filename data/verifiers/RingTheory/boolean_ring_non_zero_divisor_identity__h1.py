import sympy
from sympy.abc import x, y, z
import itertools

class FiniteRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        
    def add(self, a, b):
        return (a + b) % self.n
        
    def mul(self, a, b):
        return (a * b) % self.n
        
    def __repr__(self):
        return f"Z_{self.n}"

# Standard finite rings for potential counterexamples
Z2 = FiniteRing(2)
Z3 = FiniteRing(3)
Z4 = FiniteRing(4)
Z5 = FiniteRing(5)
Z6 = FiniteRing(6)
Z7 = FiniteRing(7)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should represent a ring R and an element a.
    It can be a tuple (ring, a) where ring has `elements`, `zero`, `add`, `mul`,
    or a tuple (elements, add_func, mul_func, zero, a).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                ring, a = witness
                raw_elements = ring.elements
                zero = ring.zero
                add = ring.add
                mul = ring.mul
            elif len(witness) == 5:
                raw_elements, add, mul, zero, a = witness
            else:
                return [False, False, False]
        elif hasattr(witness, 'ring') and hasattr(witness, 'a'):
            ring = witness.ring
            a = witness.a
            raw_elements = ring.elements
            zero = ring.zero
            add = ring.add
            mul = ring.mul
        else:
            return [False, False, False]
            
        # Safely extract elements, preventing infinite loops for infinite rings
        elements_iter = iter(raw_elements)
        elements = []
        for _ in range(1001):
            try:
                elements.append(next(elements_iter))
            except StopIteration:
                break
        else:
            # If we reach here, the ring is too large or infinite
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H_1: a is a non-zero element of R
    try:
        h1 = (a in elements) and (a != zero)
    except Exception:
        h1 = False

    # H_2: a is not a zero divisor in R
    try:
        h2 = True
        for e in elements:
            if e != zero:
                if mul(a, e) == zero or mul(e, a) == zero:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The ring R does NOT have a multiplicative identity OR a is NOT that identity element.
    # This is equivalent to saying that `a` does not act as the multiplicative identity.
    try:
        is_identity = True
        for e in elements:
            if mul(a, e) != e or mul(e, a) != e:
                is_identity = False
                break
        neg_q = not is_identity
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is a non-zero element of R",
    "H_2: a is not a zero divisor in R",
    "¬Q: R does not have a multiplicative identity or a is not that identity"
]

N_HYP = 2
NEG_Q_INDEX = 2