import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, x_elem = witness
        elif isinstance(witness, dict) and 'R' in witness and 'x' in witness:
            R_obj = witness['R']
            x_elem = witness['x']
        elif hasattr(witness, 'R') and hasattr(witness, 'x'):
            R_obj = witness.R
            x_elem = witness.x
        else:
            return [False] * 4

        # Case 1: R is represented by an integer n (Z/nZ)
        if isinstance(R_obj, int) and isinstance(x_elem, int):
            n = R_obj
            h1 = (n > 0)
            h2 = True
            h3 = True
            
            if n == 1:
                is_unit = True
                is_zero_divisor = False
            elif n > 1:
                x_mod = x_elem % n
                is_unit = (math.gcd(x_mod, n) == 1)
                is_zero_divisor = (x_mod != 0) and (math.gcd(x_mod, n) > 1)
            else:
                is_unit = False
                is_zero_divisor = False
                
            neg_q = not (is_unit or is_zero_divisor)
            return [h1, h2, h3, neg_q]
            
        # Case 2: R is a custom ring object
        elif hasattr(R_obj, 'elements') and hasattr(R_obj, 'add') and hasattr(R_obj, 'mul'):
            elements = list(R_obj.elements)
            h1 = len(elements) > 0
            
            if x_elem not in elements:
                return [False] * 4
                
            h2 = True
            for a in elements:
                for b in elements:
                    if R_obj.mul(a, b) != R_obj.mul(b, a):
                        h2 = False
                        break
                if not h2: break
            
            h3 = False
            one = None
            for e in elements:
                is_id = True
                for a in elements:
                    if R_obj.mul(e, a) != a or R_obj.mul(a, e) != a:
                        is_id = False
                        break
                if is_id:
                    h3 = True
                    one = e
                    break
            
            zero = None
            for e in elements:
                is_z = True
                for a in elements:
                    if R_obj.add(e, a) != a:
                        is_z = False
                        break
                if is_z:
                    zero = e
                    break
            
            is_unit = False
            if h3 and one is not None:
                for y_elem in elements:
                    if R_obj.mul(x_elem, y_elem) == one and R_obj.mul(y_elem, x_elem) == one:
                        is_unit = True
                        break
            
            is_zero_divisor = False
            if zero is not None and x_elem != zero:
                for y_elem in elements:
                    if y_elem != zero:
                        if R_obj.mul(x_elem, y_elem) == zero or R_obj.mul(y_elem, x_elem) == zero:
                            is_zero_divisor = True
                            break
            
            neg_q = not (is_unit or is_zero_divisor)
            return [h1, h2, h3, neg_q]
            
    except Exception:
        pass
    return [False] * 4

CONDITION_LABELS = [
    "H_1: R is a finite ring",
    "H_2: R is a commutative ring",
    "H_3: R has a multiplicative identity",
    "¬Q: x is neither a unit nor a zero divisor in R"
]

N_HYP = 3
NEG_Q_INDEX = 3