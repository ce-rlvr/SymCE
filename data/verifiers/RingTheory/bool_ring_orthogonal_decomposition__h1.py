import sympy
from sympy import Rational, Integer
from sympy.abc import *
import itertools
import functools
import math

# Top-level setup
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Format 1: witness is (n, x, y) representing the ring Z/nZ and elements x, y
        if isinstance(witness, (tuple, list)) and len(witness) == 3 and all(isinstance(i, int) for i in witness):
            n, x, y = witness
            h1 = n >= 2 and 0 <= x < n and 0 <= y < n
            
            ideal_y = set((k * y) % n for k in range(n))
            valid_pairs = 0
            for a in ideal_y:
                for b in range(n):
                    if (a + b) % n == x and (b * y) % n == 0:
                        valid_pairs += 1
            neg_q = valid_pairs != 1

        # Format 2: witness is (elements, add_func, mul_func, zero, x, y)
        elif isinstance(witness, (tuple, list)) and len(witness) == 6:
            elements, add, mul, zero, x, y = witness
            
            # Check if x and y are in the ring
            h1 = False
            for e in elements:
                if e == x:
                    h1 = True
                    break
            if h1:
                h1_y = False
                for e in elements:
                    if e == y:
                        h1_y = True
                        break
                h1 = h1 and h1_y
            
            # Generate the principal ideal (y) assuming a commutative ring (or left ideal)
            ideal_y = []
            for k in elements:
                ky = mul(k, y)
                if ky not in ideal_y:
                    ideal_y.append(ky)
                    
            valid_pairs = 0
            for a in ideal_y:
                for b in elements:
                    if add(a, b) == x and mul(b, y) == zero:
                        valid_pairs += 1
            neg_q = valid_pairs != 1
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of R",
    "¬Q: There do not exist unique elements a, b in R such that x = a + b, a in (y), and by = 0"
]

N_HYP = 1
NEG_Q_INDEX = 1