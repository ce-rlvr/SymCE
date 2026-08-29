import sympy
from sympy import eye, zeros
import itertools
import math
import functools

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_prop_or_method(obj, name):
    attr = getattr(obj, name, None)
    if attr is None and name == 'is_ring':
        attr = getattr(obj, 'is_Ring', None)
    if attr is None:
        return None
    if callable(attr):
        try:
            return attr()
        except Exception:
            return None
    return attr

def get_ring_ops(witness):
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
        elements_iter = witness.elements
        if callable(elements_iter):
            elements_iter = elements_iter()
        
        elements = []
        for i, e in enumerate(elements_iter):
            if i > 1000:
                return None, None, None, None
            elements.append(e)
        return elements, witness.add, witness.mul, witness.zero
    
    if isinstance(witness, (list, tuple, set)):
        elements = []
        for i, e in enumerate(witness):
            if i > 1000:
                return None, None, None, None
            elements.append(e)
        
        try:
            add = lambda x, y: x + y
            mul = lambda x, y: x * y
            if elements:
                _ = add(elements[0], elements[0])
                _ = mul(elements[0], elements[0])
        except Exception:
            return None, None, None, None
            
        zero = None
        for e in elements:
            try:
                if all(add(e, x) == x for x in elements):
                    zero = e
                    break
            except Exception:
                pass
        return elements, add, mul, zero
    return None, None, None, None

def is_ring(elements, add, mul, zero):
    if zero is None: 
        return False
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: 
            return False
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        
        for b in elements:
            ab_add = add(a, b)
            ab_mul = mul(a, b)
            if ab_add not in elements: return False
            if ab_mul not in elements: return False
            if ab_add != add(b, a): return False
            
            for c in elements:
                if add(ab_add, c) != add(a, add(b, c)): return False
                if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
                if mul(ab_add, c) != add(mul(a, c), mul(b, c)): return False
    return True

def jacobson_radical(elements, add, mul, zero):
    def is_left_quasi_regular(a):
        for b in elements:
            if add(b, a) == mul(b, a):
                return True
        return False

    J = []
    for x in elements:
        x_in_J = True
        for y in elements:
            yx = mul(y, x)
            if not is_left_quasi_regular(yx):
                x_in_J = False
                break
        if x_in_J:
            J.append(x)
    return J

def is_nilpotent_ideal(I, elements, add, mul, zero):
    if not I:
        return True
    
    current_power = list(I)
    
    for _ in range(len(elements) + 1):
        if all(x == zero for x in current_power):
            return True
        
        next_prods = []
        for a in I:
            for b in current_power:
                next_prods.append(mul(a, b))
        
        span = []
        for x in next_prods:
            if x not in span:
                span.append(x)
        
        added = True
        while added:
            added = False
            new_elements = []
            for x in span:
                for y in span:
                    s = add(x, y)
                    if s not in span and s not in new_elements:
                        new_elements.append(s)
            if new_elements:
                span.extend(new_elements)
                added = True
        
        current_power = span
        
    return all(x == zero for x in current_power)

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        val = check_prop_or_method(witness, 'is_ring')
        if val is not None:
            h1 = bool(val)
        else:
            elements, add, mul, zero = get_ring_ops(witness)
            if elements is not None:
                h1 = is_ring(elements, add, mul, zero)
    except Exception:
        pass

    h2 = False
    try:
        val = check_prop_or_method(witness, 'is_left_artinian')
        if val is not None:
            h2 = bool(val)
        else:
            elements, add, mul, zero = get_ring_ops(witness)
            if elements is not None:
                h2 = True
    except Exception:
        pass

    neg_q = False
    try:
        val = check_prop_or_method(witness, 'jacobson_radical_is_nilpotent')
        if val is not None:
            neg_q = not bool(val)
        else:
            val = check_prop_or_method(witness, 'J_is_nilpotent')
            if val is not None:
                neg_q = not bool(val)
            else:
                elements, add, mul, zero = get_ring_ops(witness)
                if elements is not None:
                    J = jacobson_radical(elements, add, mul, zero)
                    neg_q = not is_nilpotent_ideal(J, elements, add, mul, zero)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a left Artinian ring",
    "¬Q: J(R) is not a nilpotent ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2