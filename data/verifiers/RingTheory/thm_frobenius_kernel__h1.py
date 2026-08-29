import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    Expected witness structure (duck-typing):
    An object or dictionary with:
      - elements: iterable of ring elements
      - p: integer (the power for the Frobenius endomorphism)
      - zero: the additive identity (optional, defaults to elements[0] - elements[0])
      - add: function(a, b) -> a + b (optional, defaults to a + b)
      - mul: function(a, b) -> a * b (optional, defaults to a * b)
    Alternatively, a tuple (R, p) where R is a ring object or list of elements.
    """
    try:
        if isinstance(witness, dict):
            elements = list(witness['elements'])
            p = witness['p']
            zero = witness['zero']
            add = witness['add']
            mul = witness['mul']
        elif isinstance(witness, tuple):
            R, p = witness
            if isinstance(R, list):
                elements = R
                zero = elements[0] - elements[0]
                add = lambda a, b: a + b
                mul = lambda a, b: a * b
            else:
                elements = list(R.elements)
                zero = getattr(R, 'zero', elements[0] - elements[0])
                add = getattr(R, 'add', lambda a, b: a + b)
                mul = getattr(R, 'mul', lambda a, b: a * b)
        else:
            elements = list(witness.elements)
            p = witness.p
            zero = getattr(witness, 'zero', elements[0] - elements[0])
            add = getattr(witness, 'add', lambda a, b: a + b)
            mul = getattr(witness, 'mul', lambda a, b: a * b)
    except Exception:
        return [False, False, False]

    def power(x, n):
        if n <= 0:
            raise ValueError("n must be positive")
        res = None
        base = x
        while n > 0:
            if n % 2 == 1:
                if res is None:
                    res = base
                else:
                    res = mul(res, base)
            base = mul(base, base)
            n //= 2
        return res

    # H_1: R is a reduced ring
    # A finite ring is reduced if it has no non-zero nilpotent elements.
    h1 = False
    try:
        h1 = True
        n_elements = len(elements)
        if n_elements > 0:
            for x in elements:
                if x != zero:
                    if power(x, n_elements) == zero:
                        h1 = False
                        break
    except Exception:
        h1 = False

    if not isinstance(p, int) or p <= 0:
        return [h1, False, False]

    # H_2: F(x) = x^p is an endomorphism
    h2 = False
    try:
        h2 = True
        for x in elements:
            for y in elements:
                # F(x+y) == F(x) + F(y)
                x_plus_y = add(x, y)
                f_x_plus_y = power(x_plus_y, p)
                
                f_x = power(x, p)
                f_y = power(y, p)
                fx_plus_fy = add(f_x, f_y)
                
                if f_x_plus_y != fx_plus_fy:
                    h2 = False
                    break
                
                # F(xy) == F(x)F(y)
                xy = mul(x, y)
                f_xy = power(xy, p)
                fx_fy = mul(f_x, f_y)
                
                if f_xy != fx_fy:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: The kernel of F is not the trivial ideal {0}
    # i.e., there exists some x != 0 such that F(x) = 0
    neg_q = False
    try:
        for x in elements:
            if x != zero:
                if power(x, p) == zero:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "H_2: F(x) = x^p is an endomorphism",
    "¬Q: The kernel of F is not the trivial ideal {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2