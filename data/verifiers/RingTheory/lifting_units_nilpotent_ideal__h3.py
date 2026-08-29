import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
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

def is_eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            x = witness['x']
            add = witness.get('add', lambda a, b: a + b)
            mul = witness.get('mul', lambda a, b: a * b)
            sub = witness.get('sub', lambda a, b: a - b)
            eq = witness.get('eq', is_eq)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            R = witness[0]
            I = witness[1]
            x = witness[2]
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            sub = lambda a, b: a - b
            eq = is_eq
        else:
            R = witness.R
            I = witness.I
            x = witness.x
            add = getattr(witness, 'add', lambda a, b: a + b)
            mul = getattr(witness, 'mul', lambda a, b: a * b)
            sub = getattr(witness, 'sub', lambda a, b: a - b)
            eq = getattr(witness, 'eq', is_eq)
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring with identity
    try:
        R_list = []
        for i, elem in enumerate(R):
            if i > 500:
                raise ValueError("Ring too large")
            R_list.append(elem)
        if not R_list:
            h1 = False
        else:
            zero = None
            for z in R_list:
                if all(eq(add(z, a), a) and eq(add(a, z), a) for a in R_list):
                    zero = z
                    break
            
            one = None
            for e in R_list:
                if all(eq(mul(e, a), a) and eq(mul(a, e), a) for a in R_list):
                    one = e
                    break
            
            if zero is None or one is None:
                h1 = False
            else:
                closed = True
                for a in R_list:
                    if not closed: break
                    for b in R_list:
                        if not any(eq(add(a, b), c) for c in R_list): 
                            closed = False
                            break
                        if not any(eq(mul(a, b), c) for c in R_list): 
                            closed = False
                            break
                        if not any(eq(sub(a, b), c) for c in R_list): 
                            closed = False
                            break
                h1 = closed
    except Exception:
        h1 = False

    # H2: I is a nilpotent two-sided ideal of R
    try:
        if not h1:
            h2 = False
        else:
            I_list = []
            for i, elem in enumerate(I):
                if i > 500:
                    raise ValueError("Ideal too large")
                I_list.append(elem)
            if not I_list:
                h2 = False
            else:
                is_subset = all(any(eq(a, r) for r in R_list) for a in I_list)
                if not is_subset:
                    h2 = False
                else:
                    is_ideal = True
                    for a in I_list:
                        if not is_ideal: break
                        for b in I_list:
                            if not any(eq(add(a, b), c) for c in I_list): 
                                is_ideal = False
                                break
                            if not any(eq(sub(a, b), c) for c in I_list): 
                                is_ideal = False
                                break
                    for a in I_list:
                        if not is_ideal: break
                        for r in R_list:
                            if not any(eq(mul(r, a), c) for c in I_list): 
                                is_ideal = False
                                break
                            if not any(eq(mul(a, r), c) for c in I_list): 
                                is_ideal = False
                                break
                    
                    if not is_ideal:
                        h2 = False
                    else:
                        current_prods = I_list
                        is_nilp = False
                        for _ in range(len(R_list) + 1):
                            if all(eq(p, zero) for p in current_prods):
                                is_nilp = True
                                break
                            next_prods = []
                            for p in current_prods:
                                for a in I_list:
                                    prod = mul(p, a)
                                    if not any(eq(prod, x_val) for x_val in next_prods):
                                        next_prods.append(prod)
                            current_prods = next_prods
                        
                        if not is_nilp:
                            is_nilp = all(eq(p, zero) for p in current_prods)
                        h2 = is_nilp
    except Exception:
        h2 = False

    # H3: The image of x in R/I is a unit in R/I
    try:
        if not h1 or not h2:
            h3 = False
        else:
            if not any(eq(x, r) for r in R_list):
                h3 = False
            else:
                h3 = False
                for y in R_list:
                    xy = mul(x, y)
                    yx = mul(y, x)
                    xy_minus_1 = sub(xy, one)
                    yx_minus_1 = sub(yx, one)
                    
                    xy_in_I = any(eq(xy_minus_1, a) for a in I_list)
                    yx_in_I = any(eq(yx_minus_1, a) for a in I_list)
                    
                    if xy_in_I and yx_in_I:
                        h3 = True
                        break
    except Exception:
        h3 = False

    # neg_Q: x is NOT a unit in R
    try:
        if not h1:
            neg_q = False
        else:
            is_unit = False
            for y in R_list:
                if eq(mul(x, y), one) and eq(mul(y, x), one):
                    is_unit = True
                    break
            neg_q = not is_unit
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I is a nilpotent two-sided ideal of R",
    "H_3: The image of x in R/I is a unit in R/I",
    "¬Q: The element x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3