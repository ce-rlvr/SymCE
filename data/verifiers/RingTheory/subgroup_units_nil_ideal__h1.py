import sympy
from sympy import Matrix, eye, zeros
import itertools
import math
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is a nil ideal of R",
    "¬Q: 1+I is not a subgroup of the group of units of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
        else:
            return [False, False]
        
        R = list(R)
        I = list(I)
    except Exception:
        return [False, False]
    
    def eq(a, b):
        if hasattr(a, 'equals'):
            try:
                if a.equals(b):
                    return True
            except Exception:
                pass
        return a == b

    def add(a, b):
        return a + b

    def mul(a, b):
        return a * b

    try:
        if not R:
            return [False, False]

        is_ring = True
        for a in R:
            for b in R:
                if not any(eq(add(a, b), z) for z in R):
                    is_ring = False
                    break
                if not any(eq(mul(a, b), z) for z in R):
                    is_ring = False
                    break
                if not eq(add(a, b), add(b, a)):
                    is_ring = False
                    break
            if not is_ring: break
        if not is_ring:
            return [False, False]
            
        for a in R:
            for b in R:
                for c in R:
                    if not eq(add(add(a, b), c), add(a, add(b, c))):
                        is_ring = False
                        break
                    if not eq(mul(mul(a, b), c), mul(a, mul(b, c))):
                        is_ring = False
                        break
                    if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))):
                        is_ring = False
                        break
                    if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))):
                        is_ring = False
                        break
                if not is_ring: break
            if not is_ring: break
            
        if not is_ring:
            return [False, False]

        zero = None
        for x in R:
            if all(eq(add(x, y), y) for y in R):
                zero = x
                break
        if zero is None:
            return [False, False]

        h1 = True
        if not I:
            h1 = False
            
        if h1:
            for x in I:
                if not any(eq(x, y) for y in R):
                    h1 = False
                    break
        
        if h1:
            for x in I:
                for y in I:
                    s = add(x, y)
                    if not any(eq(s, z) for z in I):
                        h1 = False
                        break
                if not h1: break

        if h1:
            for x in I:
                for r in R:
                    p1 = mul(x, r)
                    p2 = mul(r, x)
                    if not any(eq(p1, z) for z in I):
                        h1 = False
                        break
                    if not any(eq(p2, z) for z in I):
                        h1 = False
                        break
                if not h1: break

        if h1:
            for x in I:
                is_nil = False
                p = x
                for _ in range(len(R) + 1):
                    if eq(p, zero):
                        is_nil = True
                        break
                    p = mul(p, x)
                if not is_nil:
                    h1 = False
                    break

        identity = None
        for x in R:
            if all(eq(mul(x, y), y) and eq(mul(y, x), y) for y in R):
                identity = x
                break
        
        if identity is None:
            neg_q = True
        else:
            U_R = []
            for x in R:
                inv_exists = False
                for y in R:
                    if eq(mul(x, y), identity) and eq(mul(y, x), identity):
                        inv_exists = True
                        break
                if inv_exists:
                    U_R.append(x)
            
            one_plus_I = []
            for x in I:
                one_plus_I.append(add(identity, x))
                
            is_subgroup = True
            if len(one_plus_I) == 0:
                is_subgroup = False
            else:
                for x in one_plus_I:
                    if not any(eq(x, u) for u in U_R):
                        is_subgroup = False
                        break
                
                if is_subgroup:
                    for x in one_plus_I:
                        for y in one_plus_I:
                            p = mul(x, y)
                            if not any(eq(p, z) for z in one_plus_I):
                                is_subgroup = False
                                break
                        if not is_subgroup: break
                
                if is_subgroup:
                    for x in one_plus_I:
                        inv = None
                        for y in U_R:
                            if eq(mul(x, y), identity) and eq(mul(y, x), identity):
                                inv = y
                                break
                        if inv is None:
                            is_subgroup = False
                            break
                        if not any(eq(inv, z) for z in one_plus_I):
                            is_subgroup = False
                            break
            
            neg_q = not is_subgroup

        return [h1, neg_q]
    except Exception:
        return [False, False]