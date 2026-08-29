import itertools
import functools

# Top-level setup
# Witnesses are expected to be tuples: (elements, add_func, mul_func, I_elements, J_elements)
# where elements is a list of ring elements, add_func and mul_func are binary operations,
# and I_elements, J_elements are lists representing the ideals I and J.

def _is_boolean_ring(elements, add, mul):
    if not elements:
        return False
    
    # Check closure
    for x in elements:
        for y in elements:
            if add(x, y) not in elements: return False
            if mul(x, y) not in elements: return False
            
    # Check commutativity and associativity of addition, associativity of multiplication, distributivity
    for x in elements:
        for y in elements:
            if add(x, y) != add(y, x): return False
            for z in elements:
                if add(x, add(y, z)) != add(add(x, y), z): return False
                if mul(x, mul(y, z)) != mul(mul(x, y), z): return False
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): return False
                
    # Check additive identity
    zeros = [z for z in elements if all(add(z, x) == x for x in elements)]
    if not zeros: return False
    zero = zeros[0]
    
    # Check additive inverses
    for x in elements:
        if not any(add(x, y) == zero for y in elements): return False
        
    # Check Boolean ring property: x^2 = x
    for x in elements:
        if mul(x, x) != x: return False
        
    return True

def _is_ideal(elements, add, mul, I):
    if not I:
        return False
    # Check additive closure
    for x in I:
        for y in I:
            if add(x, y) not in I: return False
    # Check absorption
    for x in I:
        for r in elements:
            if mul(r, x) not in I: return False
            if mul(x, r) not in I: return False
    # Check additive inverse closure
    zeros = [z for z in elements if all(add(z, x) == x for x in elements)]
    if zeros:
        zero = zeros[0]
        for x in I:
            inverses = [y for y in elements if add(x, y) == zero]
            if not any(inv in I for inv in inverses): return False
    return True

def _get_product_ideal(elements, add, mul, I, J):
    prods = set()
    for i in I:
        for j in J:
            prods.add(mul(i, j))
            
    closure = set(prods)
    added = True
    while added:
        added = False
        new_elements = set()
        for x in closure:
            for y in closure:
                s = add(x, y)
                if s not in closure and s not in new_elements:
                    new_elements.add(s)
        if new_elements:
            closure.update(new_elements)
            added = True
    return closure

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, I, J = witness
        h1_ok = _is_boolean_ring(elements, add, mul) and _is_ideal(elements, add, mul, I) and _is_ideal(elements, add, mul, J)
    except Exception:
        h1_ok = False

    try:
        elements, add, mul, I, J = witness
        intersection = set(x for x in I if x in J)
        product_ideal = _get_product_ideal(elements, add, mul, I, J)
        neg_q_ok = intersection != product_ideal
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS: list[str] = [
    "H_1: R is a Boolean ring and I, J are ideals",
    "¬Q: The intersection I \\cap J is not equal to the product ideal IJ"
]

N_HYP: int = 1
NEG_Q_INDEX: int = 1