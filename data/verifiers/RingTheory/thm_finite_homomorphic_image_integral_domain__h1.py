import sympy
from sympy import Rational, Integer
import math
import itertools
import functools

class IntegerRing:
    def __init__(self):
        self.zero = 0
        self.one = 1
        self.is_integral_domain = True
        self.is_finite = False
        self.is_field = False
        self.test_elements = [-3, -2, -1, 0, 1, 2, 3]
        
    def add(self, x, y): return x + y
    def mul(self, x, y): return x * y
    def eq(self, x, y): return x == y
    def has_inverse(self, x): return x in (1, -1)

class RationalField:
    def __init__(self):
        self.zero = 0
        self.one = 1
        self.is_integral_domain = True
        self.is_finite = False
        self.is_field = True
        self.test_elements = [-2, -1, 0, 1, 2, 0.5, -0.5]
        
    def add(self, x, y): return x + y
    def mul(self, x, y): return x * y
    def eq(self, x, y): return x == y
    def has_inverse(self, x): return x != 0

class FiniteField5:
    def __init__(self):
        self.zero = 0
        self.one = 1
        self.is_integral_domain = True
        self.is_finite = True
        self.is_field = True
        self.elements = [0, 1, 2, 3, 4]
        self.test_elements = self.elements
        
    def add(self, x, y): return (x + y) % 5
    def mul(self, x, y): return (x * y) % 5
    def eq(self, x, y): return (x % 5) == (y % 5)
    def has_inverse(self, x): return (x % 5) != 0

ZZ = IntegerRing()
QQ = RationalField()
F5 = FiniteField5()

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, f = witness
        elif isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            f = witness['f']
        elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'f'):
            R = witness.R
            S = witness.S
            f = witness.f
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: S is an integral domain
    try:
        h1 = bool(S.is_integral_domain)
    except Exception:
        h1 = False
        
    # H2: f: R -> S is a ring homomorphism such that f(1_R) = 1_S
    try:
        h2 = True
        if not S.eq(f(R.one), S.one):
            h2 = False
            
        elements_to_test = getattr(R, 'elements', getattr(R, 'test_elements', []))
        if not elements_to_test:
            h2 = False
            
        for x in elements_to_test:
            for y in elements_to_test:
                if not S.eq(f(R.add(x, y)), S.add(f(x), f(y))):
                    h2 = False
                if not S.eq(f(R.mul(x, y)), S.mul(f(x), f(y))):
                    h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: f(R) is NOT a finite field
    try:
        elements_to_test = getattr(R, 'elements', getattr(R, 'test_elements', []))
        image_test = [f(x) for x in elements_to_test]
        unique_image = []
        for img in image_test:
            if not any(S.eq(img, u) for u in unique_image):
                unique_image.append(img)
                
        is_finite_field = True
        
        # 1. Check if any element in the image lacks an inverse in S
        for img in unique_image:
            if not S.eq(img, S.zero):
                if hasattr(S, 'has_inverse') and not S.has_inverse(img):
                    is_finite_field = False
                    break
                    
        if is_finite_field:
            # 2. Check if unique_image is closed under addition and multiplication
            is_closed = True
            for a in unique_image:
                for b in unique_image:
                    sum_ab = S.add(a, b)
                    if not any(S.eq(sum_ab, u) for u in unique_image):
                        is_closed = False
                        break
                if not is_closed:
                    break
                    
            if is_closed:
                for a in unique_image:
                    for b in unique_image:
                        mul_ab = S.mul(a, b)
                        if not any(S.eq(mul_ab, u) for u in unique_image):
                            is_closed = False
                            break
                    if not is_closed:
                        break
                        
            if not is_closed:
                # If it's not closed, f(R) is strictly larger than unique_image.
                # For our test rings, this implies f(R) is infinite.
                is_finite_field = False
            else:
                # 3. If closed, unique_image is exactly f(R). Check if it's a field.
                for a in unique_image:
                    if not S.eq(a, S.zero):
                        has_inv = False
                        for b in unique_image:
                            if S.eq(S.mul(a, b), S.one):
                                has_inv = True
                                break
                        if not has_inv:
                            is_finite_field = False
                            break
                            
        neg_q = not is_finite_field
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is an integral domain",
    "H_2: f: R -> S is a ring homomorphism such that f(1_R) = 1_S",
    "¬Q: The image f(R) is not a finite field"
]

N_HYP = 2
NEG_Q_INDEX = 2