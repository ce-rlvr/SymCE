import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2,2)
O3 = sympy.zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                m, x, y = witness
            elif len(witness) == 4:
                _, m, x, y = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if not (isinstance(m, int) and isinstance(x, int) and isinstance(y, int)):
            return [False, False, False, False]
            
        if m <= 0:
            return [False, False, False, False]
            
        h1 = True
        h2 = True
        h3 = True
        
        def ann_gen(val):
            return m // math.gcd(val % m, m)
            
        def lcm(a, b):
            if a == 0 and b == 0:
                return 0
            return abs(a * b) // math.gcd(a, b)
            
        gen_x = ann_gen(x)
        gen_y = ann_gen(y)
        gen_xy = ann_gen(x + y)
        
        int_xy = lcm(gen_x, gen_y)
        
        neg_q = bool(gen_xy != int_xy)
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: x and y are elements of M",
    "¬Q: Ann_R(x+y) is not equal to Ann_R(x) ∩ Ann_R(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3