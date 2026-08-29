import sympy
from sympy import eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        elements = list(witness)
        if not elements:
            return [False, False]
            
        is_ring = True
        for a in elements:
            if -a not in elements:
                is_ring = False
                break
            for b in elements:
                if a + b not in elements:
                    is_ring = False
                    break
                if a * b not in elements:
                    is_ring = False
                    break
            if not is_ring:
                break
        h1_ok = is_ring
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            C = []
            for a in elements:
                for b in elements:
                    comm = a * b - b * a
                    if comm not in C:
                        C.append(comm)
            
            changed = True
            while changed:
                changed = False
                new_C = list(C)
                for c1 in C:
                    for c2 in C:
                        if c1 + c2 not in new_C:
                            new_C.append(c1 + c2)
                            changed = True
                for c in C:
                    for r in elements:
                        if r * c not in new_C:
                            new_C.append(r * c)
                            changed = True
                        if c * r not in new_C:
                            new_C.append(c * r)
                            changed = True
                C = new_C
                
            is_comm = True
            for a in elements:
                for b in elements:
                    if a * b - b * a not in C:
                        is_comm = False
                        break
                if not is_comm:
                    break
            
            neg_q = not is_comm
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: The quotient ring R/C is not a commutative ring"
]

N_HYP = 1
NEG_Q_INDEX = 1