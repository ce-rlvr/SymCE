import sympy
import math
import itertools
import functools

class Ring:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func
        self.zero = zero

Z2 = Ring([0, 1], lambda x, y: (x + y) % 2, lambda x, y: (x * y) % 2, 0)
Z3 = Ring([0, 1, 2], lambda x, y: (x + y) % 3, lambda x, y: (x * y) % 3, 0)
Z4 = Ring([0, 1, 2, 3], lambda x, y: (x + y) % 4, lambda x, y: (x * y) % 4, 0)
Z6 = Ring([0, 1, 2, 3, 4, 5], lambda x, y: (x + y) % 6, lambda x, y: (x * y) % 6, 0)
Z8 = Ring([0, 1, 2, 3, 4, 5, 6, 7], lambda x, y: (x + y) % 8, lambda x, y: (x * y) % 8, 0)

def conditions(witness) -> list[bool]:
    try:
        # Allow witness to be either a tuple (n, I, J) for Z_n, or (Ring_obj, I, J)
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
            n, I, J = witness
            elements = list(range(n))
            add = lambda a, b: (a + b) % n
            mul = lambda a, b: (a * b) % n
            zero = 0
        else:
            R, I, J = witness
            elements = R.elements
            add = R.add
            mul = R.mul
            zero = R.zero
    except Exception:
        return [False] * 5

    # H1: R is a commutative ring
    h1 = True
    try:
        for a in elements:
            if add(a, zero) != a: h1 = False
            if mul(a, zero) != zero: h1 = False
            for b in elements:
                if add(a, b) not in elements: h1 = False
                if mul(a, b) not in elements: h1 = False
                if add(a, b) != add(b, a): h1 = False
                if mul(a, b) != mul(b, a): h1 = False
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(a, add(b, c)) != add(add(a, b), c): h1 = False
                    if mul(a, mul(b, c)) != mul(mul(a, b), c): h1 = False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
        # Check additive inverses
        for a in elements:
            has_inv = False
            for b in elements:
                if add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: h1 = False
        # Check identity
        has_id = False
        for e in elements:
            is_id = True
            for a in elements:
                if mul(e, a) != a:
                    is_id = False
                    break
            if is_id:
                has_id = True
                break
        if not has_id:
            h1 = False
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    h2 = True
    try:
        if not set(I).issubset(set(elements)): h2 = False
        if zero not in I: h2 = False
        for i in I:
            for j in I:
                if add(i, j) not in I: h2 = False
            for r in elements:
                if mul(r, i) not in I: h2 = False
        for i in I:
            has_inv = False
            for j in I:
                if add(i, j) == zero:
                    has_inv = True
                    break
            if not has_inv: h2 = False
    except Exception:
        h2 = False

    # H3: The product ideal IJ is the zero ideal
    h3 = True
    try:
        # Check that J is an ideal
        if not set(J).issubset(set(elements)): h3 = False
        if zero not in J: h3 = False
        for j in J:
            for k in J:
                if add(j, k) not in J: h3 = False
            for r in elements:
                if mul(r, j) not in J: h3 = False
        for j in J:
            has_inv = False
            for k in J:
                if add(j, k) == zero:
                    has_inv = True
                    break
            if not has_inv: h3 = False
            
        # Check that IJ = {0}
        for i in I:
            for j in J:
                if mul(i, j) != zero:
                    h3 = False
    except Exception:
        h3 = False

    # H4: I is not the zero ideal
    h4 = True
    try:
        if set(I) == {zero}: h4 = False
        if not I: h4 = False
    except Exception:
        h4 = False

    # neg_Q: NOT every element of J is a zero-divisor in R
    neg_q = False
    try:
        # A zero-divisor is a non-zero element 'a' such that 'ab = 0' for some non-zero 'b'.
        def is_zero_divisor(x):
            if x == zero:
                return False
            for y in elements:
                if y != zero and mul(x, y) == zero:
                    return True
            return False
        
        for j in J:
            if not is_zero_divisor(j):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: The product ideal IJ is the zero ideal",
    "H_4: I is not the zero ideal",
    "¬Q: Not every element of J is a zero-divisor in R"
]

N_HYP = 4
NEG_Q_INDEX = 4