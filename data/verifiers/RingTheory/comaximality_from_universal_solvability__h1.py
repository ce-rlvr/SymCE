import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def get_attr_or_key(obj, name):
    if isinstance(obj, dict):
        return obj[name]
    return getattr(obj, name)

def get_add(witness):
    if hasattr(witness, 'add') and callable(witness.add):
        return witness.add
    if isinstance(witness, dict) and callable(witness.get('add')):
        return witness['add']
    add_table = get_attr_or_key(witness, 'add')
    elements = list(get_attr_or_key(witness, 'elements'))
    return lambda a, b: add_table[elements.index(a)][elements.index(b)]

def get_mul(witness):
    if hasattr(witness, 'mul') and callable(witness.mul):
        return witness.mul
    if isinstance(witness, dict) and callable(witness.get('mul')):
        return witness['mul']
    mul_table = get_attr_or_key(witness, 'mul')
    elements = list(get_attr_or_key(witness, 'elements'))
    return lambda a, b: mul_table[elements.index(a)][elements.index(b)]

def conditions(witness) -> list[bool]:
    try:
        elements = list(get_attr_or_key(witness, 'elements'))
        I = list(get_attr_or_key(witness, 'I'))
        J = list(get_attr_or_key(witness, 'J'))
        add = get_add(witness)
        mul = get_mul(witness)
    except Exception:
        return [False, False, False]

    # H_1: I and J are ideals of R
    try:
        h1 = True
        n = len(elements)
        if n == 0:
            h1 = False
        else:
            # Check R is a ring
            for a in elements:
                for b in elements:
                    if add(a, b) != add(b, a): h1 = False
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): h1 = False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): h1 = False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): h1 = False
            
            zero = None
            for e in elements:
                if all(add(e, x) == x for x in elements):
                    zero = e
                    break
            if zero is None:
                h1 = False
            else:
                # Check additive inverses
                for a in elements:
                    if not any(add(a, x) == zero for x in elements):
                        h1 = False
                
                # Check I is an ideal
                if zero not in I: h1 = False
                for i in I:
                    for j in I:
                        if add(i, j) not in I: h1 = False
                    has_inv = False
                    for x in I:
                        if add(i, x) == zero:
                            has_inv = True
                            break
                    if not has_inv: h1 = False
                    for r in elements:
                        if mul(r, i) not in I: h1 = False
                        if mul(i, r) not in I: h1 = False
                
                # Check J is an ideal
                if zero not in J: h1 = False
                for j in J:
                    for k in J:
                        if add(j, k) not in J: h1 = False
                    has_inv = False
                    for x in J:
                        if add(j, x) == zero:
                            has_inv = True
                            break
                    if not has_inv: h1 = False
                    for r in elements:
                        if mul(r, j) not in J: h1 = False
                        if mul(j, r) not in J: h1 = False
    except Exception:
        h1 = False

    # H_2: Universal solvability of simultaneous congruences
    try:
        h2 = True
        for a in elements:
            for b in elements:
                solvable = False
                for x in elements:
                    x_minus_a_in_I = False
                    for i in I:
                        if add(a, i) == x:
                            x_minus_a_in_I = True
                            break
                    if not x_minus_a_in_I:
                        continue
                    
                    x_minus_b_in_J = False
                    for j in J:
                        if add(b, j) == x:
                            x_minus_b_in_J = True
                            break
                    
                    if x_minus_a_in_I and x_minus_b_in_J:
                        solvable = True
                        break
                if not solvable:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: The ideals I and J are not comaximal
    # In the context of the dropped hypothesis (R is a ring with identity),
    # comaximality requires the existence of an identity element 1 such that 1 \in I + J.
    try:
        identity = None
        for e in elements:
            is_id = True
            for x in elements:
                if mul(e, x) != x or mul(x, e) != x:
                    is_id = False
                    break
            if is_id:
                identity = e
                break
        
        if identity is None:
            neg_q = True
        else:
            id_in_sum = False
            for i in I:
                for j in J:
                    if add(i, j) == identity:
                        id_in_sum = True
                        break
                if id_in_sum:
                    break
            neg_q = not id_in_sum
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: Universal solvability of simultaneous congruences",
    "¬Q: The ideals I and J are not comaximal"
]
N_HYP = 2
NEG_Q_INDEX = 2