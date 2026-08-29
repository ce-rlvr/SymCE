import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# We construct a finite commutative ring R without unique factorization,
# specifically R = Z_2[X, Y, Z, W] / (X^2, Y^2, Z^2, W^2, XY - ZW, all degree >= 3 terms).
# This ring has 1024 elements and contains pairs of elements that do not have a GCD.
# Elements are represented as 10-bit integers where bits correspond to the basis:
# 0: 1, 1: X, 2: Y, 3: Z, 4: W, 5: XY=ZW, 6: XZ, 7: XW, 8: YZ, 9: YW

mul_table = [[0] * 1024 for _ in range(1024)]
divisors = [set() for _ in range(1024)]

for i in range(1024):
    a0 = i & 1
    a1 = (i >> 1) & 1
    a2 = (i >> 2) & 1
    a3 = (i >> 3) & 1
    a4 = (i >> 4) & 1
    for j in range(1024):
        b0 = j & 1
        b1 = (j >> 1) & 1
        b2 = (j >> 2) & 1
        b3 = (j >> 3) & 1
        b4 = (j >> 4) & 1
        
        # Degree 0 and Degree 1 cross terms
        base = (j if a0 else 0) ^ (i if b0 else 0) ^ (a0 & b0)
        
        # Degree 2 terms
        c5 = (a1 & b2) ^ (a2 & b1) ^ (a3 & b4) ^ (a4 & b3)
        c6 = (a1 & b3) ^ (a3 & b1)
        c7 = (a1 & b4) ^ (a4 & b1)
        c8 = (a2 & b3) ^ (a3 & b2)
        c9 = (a2 & b4) ^ (a4 & b2)
        
        res = base ^ (c5 << 5) ^ (c6 << 6) ^ (c7 << 7) ^ (c8 << 8) ^ (c9 << 9)
        mul_table[i][j] = res
        divisors[res].add(i)

class CustomRingElement:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return isinstance(other, CustomRingElement) and self.val == other.val

    def __hash__(self):
        return hash(self.val)

    def __repr__(self):
        return f"R({self.val})"

    def __add__(self, other):
        if not isinstance(other, CustomRingElement):
            return NotImplemented
        return CustomRingElement(self.val ^ other.val)

    def __mul__(self, other):
        if not isinstance(other, CustomRingElement):
            return NotImplemented
        return CustomRingElement(mul_table[self.val][other.val])

R_elements = [CustomRingElement(i) for i in range(1024)]
R_zero = R_elements[0]
R_one = R_elements[1]

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        a, b = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = (isinstance(a, CustomRingElement) and isinstance(b, CustomRingElement) and 
              (a in R_elements) and (b in R_elements) and (a != R_zero) and (b != R_zero))
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            val_a = a.val
            val_b = b.val
            
            divs_a = divisors[val_a]
            divs_b = divisors[val_b]
            
            common_divs = divs_a.intersection(divs_b)
            
            has_gcd = False
            for g in common_divs:
                # g is a GCD if every common divisor divides g
                is_gcd = True
                for d in common_divs:
                    if d not in divisors[g]:
                        is_gcd = False
                        break
                if is_gcd:
                    has_gcd = True
                    break
                    
            neg_q = not has_gcd
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "¬Q: a and b do not have a greatest common divisor in R"
]

N_HYP = 1
NEG_Q_INDEX = 1