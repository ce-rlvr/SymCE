import itertools
import functools
import math
import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def is_in(a, lst):
    return any(a == b for b in lst)

def add_to_list(lst, a):
    if not is_in(a, lst):
        lst.append(a)
        return True
    return False

def sets_equal(lst1, lst2):
    for a in lst1:
        if not is_in(a, lst2): return False
    for a in lst2:
        if not is_in(a, lst1): return False
    return True

def extract_witness(witness):
    if isinstance(witness, dict):
        R = witness.get('R')
        x = witness.get('x')
        y = witness.get('y')
        I = witness.get('I')
    elif isinstance(witness, (tuple, list)) and len(witness) == 4:
        R, x, y, I = witness[0], witness[1], witness[2], witness[3]
    else:
        R = getattr(witness, 'R', None)
        x = getattr(witness, 'x', None)
        y = getattr(witness, 'y', None)
        I = getattr(witness, 'I', None)
        
    if I is not None:
        try:
            I = list(I)
        except Exception:
            pass
            
    return R, x, y, I

def get_add_mul(witness, R):
    if isinstance(witness, dict):
        if 'add' in witness and 'mul' in witness:
            return witness['add'], witness['mul']
    if hasattr(witness, 'add') and hasattr(witness, 'mul'):
        return witness.add, witness.mul
    if hasattr(R, 'add') and hasattr(R, 'mul'):
        return R.add, R.mul
    return lambda a, b: a + b, lambda a, b: a * b

def get_zero(elements, add):
    for z in elements:
        try:
            if all(add(z, a) == a and add(a, z) == a for a in elements):
                return z
        except Exception:
            continue
    return None

def get_neg_func(elements, add, zero):
    def neg(a):
        for b in elements:
            try:
                if add(a, b) == zero and add(b, a) == zero:
                    return b
            except Exception:
                continue
        return None
    return neg

def is_boolean_ring(elements, add, mul, zero):
    if zero is None: return False
    neg = get_neg_func(elements, add, zero)
    
    for a in elements:
        if mul(a, a) != a: return False
        if neg(a) is None: return False
        for b in elements:
            s = add(a, b)
            p = mul(a, b)
            if not is_in(s, elements): return False
            if not is_in(p, elements): return False
            if s != add(b, a): return False

    for a in elements:
        for b in elements:
            ab = add(a, b)
            for c in elements:
                if add(ab, c) != add(a, add(b, c)): return False

    for a in elements:
        for b in elements:
            ab = mul(a, b)
            for c in elements:
                if mul(ab, c) != mul(a, mul(b, c)): return False

    for a in elements:
        for b in elements:
            ab_add = add(a, b)
            ab_mul = mul(a, b)
            for c in elements:
                if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
                if mul(ab_add, c) != add(mul(a, c), mul(b, c)): return False

    return True

def ideal_generated_by(gens, elements, add, mul, neg):
    ideal = []
    for g in gens:
        if is_in(g, elements):
            add_to_list(ideal, g)
    
    changed = True
    while changed:
        changed = False
        new_elements = []
        for a in ideal:
            na = neg(a)
            if na is not None and is_in(na, elements) and not is_in(na, ideal) and not is_in(na, new_elements):
                new_elements.append(na)
            for b in ideal:
                s = add(a, b)
                if is_in(s, elements) and not is_in(s, ideal) and not is_in(s, new_elements):
                    new_elements.append(s)
            for r in elements:
                p1 = mul(r, a)
                if is_in(p1, elements) and not is_in(p1, ideal) and not is_in(p1, new_elements):
                    new_elements.append(p1)
                p2 = mul(a, r)
                if is_in(p2, elements) and not is_in(p2, ideal) and not is_in(p2, new_elements):
                    new_elements.append(p2)
        if new_elements:
            for e in new_elements:
                ideal.append(e)
            changed = True
    return ideal

def conditions(witness) -> list[bool]:
    try:
        R, x, y, I = extract_witness(witness)
        if R is None: 
            return [False, False, False]
        
        elements = getattr(R, 'elements', R)
        if not isinstance(elements, (list, tuple, set)):
            elements = list(elements)
            
        add, mul = get_add_mul(witness, R)
        zero = get_zero(elements, add)
        
        if not is_in(x, elements) or not is_in(y, elements):
            return [False, False, False]
            
        # H1: R is a Boolean ring
        try:
            h1 = is_boolean_ring(elements, add, mul, zero)
        except Exception:
            h1 = False
            
        # H2: I is the ideal generated by x and y
        try:
            if zero is None:
                h2 = False
            else:
                neg = get_neg_func(elements, add, zero)
                ideal_xy = ideal_generated_by([x, y], elements, add, mul, neg)
                h2 = sets_equal(I, ideal_xy)
        except Exception:
            h2 = False
            
        # neg_Q: I is NOT the principal ideal generated by x + y + xy
        try:
            if zero is None:
                neg_q = False
            else:
                neg = get_neg_func(elements, add, zero)
                xy = mul(x, y)
                x_plus_y = add(x, y)
                z = add(x_plus_y, xy)
                ideal_z = ideal_generated_by([z], elements, add, mul, neg)
                neg_q = not sets_equal(I, ideal_z)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: I is the ideal generated by x and y",
    "¬Q: I is not the principal ideal generated by x + y + xy"
]

N_HYP = 2
NEG_Q_INDEX = 2