import math
import sympy
from sympy import Symbol, symbols
from sympy.abc import x, y, z

Z = Symbol('Z')
ZZ = Symbol('ZZ')
Q = Symbol('Q')
QQ = Symbol('QQ')
R = Symbol('R')

def int_lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2 and isinstance(witness[1], (list, tuple)):
                gens = witness[1]
            elif len(witness) > 0 and str(witness[0]) in ['Z', 'ZZ', 'Q', 'QQ', 'R', 'Integers', 'S.Integers']:
                gens = witness[1:]
            else:
                gens = witness
        elif isinstance(witness, list):
            gens = witness
        else:
            return [False, False, False]
            
        if len(gens) < 2:
            return [False, False, False]
            
        is_int = all(isinstance(g, int) or (hasattr(g, 'is_integer') and g.is_integer) for g in gens)
        
        if is_int:
            gens = [int(g) for g in gens]
            h1 = True
            h2 = True
            p = 1
            for g in gens:
                p *= g
            intersect = gens[0]
            for g in gens[1:]:
                intersect = int_lcm(intersect, g)
            neg_q = abs(p) != abs(intersect)
            return [h1, h2, neg_q]
        else:
            h1 = True
            h2 = True
            p = gens[0]
            for g in gens[1:]:
                p = p * g
            
            intersect = gens[0]
            for g in gens[1:]:
                intersect = sympy.lcm(intersect, g)
                
            if intersect == 0:
                neg_q = (p != 0)
            else:
                ratio = sympy.cancel(p / intersect)
                neg_q = not (ratio.is_number and ratio != 0)
            return [h1, h2, bool(neg_q)]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I_1, I_2, ..., I_n are ideals of R",
    "¬Q: The product ideal is not equal to the intersection ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2