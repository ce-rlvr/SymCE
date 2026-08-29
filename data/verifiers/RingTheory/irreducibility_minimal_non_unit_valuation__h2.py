import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z, t

# Top-level setup for potential witness expressions
# (No specific named rings are strictly required for this domain, but we provide standard symbols)

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: x is a non-zero non-unit in R",
    "H_3: d(x) is minimal among all non-zero non-units in R",
    "¬Q: x is not an irreducible element in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_ring_ops(witness):
    """
    Extracts ring operations and elements from the witness.
    Supports a simple tuple format (n, d_dict, x) for Z/nZ, 
    or a custom object with the required attributes.
    """
    if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
        n, d_obj, x_val = witness
        elements = list(range(n))
        zero = 0
        one = 1
        add = lambda a, b: (a + b) % n
        mul = lambda a, b: (a * b) % n
        if isinstance(d_obj, dict):
            d = lambda a: d_obj[a]
        else:
            d = d_obj
        return elements, zero, one, add, mul, d, x_val
    else:
        elements = list(witness.elements)
        zero = witness.zero
        one = witness.one
        add = witness.add
        mul = witness.mul
        d = witness.d
        x_val = witness.x
        return elements, zero, one, add, mul, d, x_val

def conditions(witness) -> list[bool]:
    try:
        elements, zero, one, add, mul, d, x_val = get_ring_ops(witness)
    except Exception:
        return [False, False, False, False]

    # Helper to check if an element is a unit
    def is_unit(a):
        for y_elem in elements:
            if mul(a, y_elem) == one:
                return True
        return False

    # H_1: R is a Euclidean domain
    h1_ok = False
    try:
        # Precompute subtraction map for fast lookup: sub_map[sum][a] = b
        sub_map = {a: {} for a in elements}
        for a in elements:
            for b in elements:
                s = add(a, b)
                sub_map[s][a] = b
                sub_map[s][b] = a
        
        is_euclid = True
        for a in elements:
            for b in elements:
                if b == zero:
                    continue
                found = False
                for q in elements:
                    bq = mul(b, q)
                    if bq in sub_map[a]:
                        r = sub_map[a][bq]
                        if r == zero or d(r) < d(b):
                            found = True
                            break
                if not found:
                    is_euclid = False
                    break
            if not is_euclid:
                break
        h1_ok = is_euclid
    except Exception:
        h1_ok = False

    # H_2: x is a non-zero non-unit in R
    h2_ok = False
    try:
        if x_val != zero and not is_unit(x_val):
            h2_ok = True
    except Exception:
        h2_ok = False

    # H_3: d(x) is minimal among all non-zero non-units in R
    h3_ok = False
    try:
        if h2_ok:
            dx = d(x_val)
            is_minimal = True
            for y_elem in elements:
                if y_elem != zero and not is_unit(y_elem):
                    if d(y_elem) < dx:
                        is_minimal = False
                        break
            h3_ok = is_minimal
    except Exception:
        h3_ok = False

    # ¬Q: x is NOT an irreducible element in R
    # An element is reducible if it can be factored into two non-units.
    neg_q_ok = False
    try:
        is_not_irreducible = False
        for a in elements:
            for b in elements:
                if mul(a, b) == x_val:
                    if not is_unit(a) and not is_unit(b):
                        is_not_irreducible = True
                        break
            if is_not_irreducible:
                break
        neg_q_ok = is_not_irreducible
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]