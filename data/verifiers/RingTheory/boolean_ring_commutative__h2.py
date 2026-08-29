import itertools
from sympy import eye, zeros, Symbol

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        elements = list(witness)
        
        is_bool = all(x * x == x for x in elements)
        if not is_bool:
            h1_ok = False
        else:
            closed_add = all(any(x + y == z for z in elements) for x in elements for y in elements)
            closed_mul = all(any(x * y == z for z in elements) for x in elements for y in elements)
            assoc_add = all((x + y) + z == x + (y + z) for x in elements for y in elements for z in elements)
            assoc_mul = all((x * y) * z == x * (y * z) for x in elements for y in elements for z in elements)
            comm_add = all(x + y == y + x for x in elements for y in elements)
            dist_left = all(x * (y + z) == (x * y) + (x * z) for x in elements for y in elements for z in elements)
            dist_right = all((x + y) * z == (x * z) + (y * z) for x in elements for y in elements for z in elements)
            has_zero = any(all(x + z == x and z + x == x for x in elements) for z in elements)
            
            h1_ok = bool(closed_add and closed_mul and assoc_add and assoc_mul and comm_add and dist_left and dist_right and has_zero)
    except Exception:
        h1_ok = False

    try:
        elements = list(witness)
        neg_q = any(x * y != y * x for x in elements for y in elements)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: x * y != y * x for some x, y in R"
]

N_HYP = 1
NEG_Q_INDEX = 1