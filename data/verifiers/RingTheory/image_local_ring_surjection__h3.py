import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for standard algebra objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_ring_data(ring):
    if isinstance(ring, (tuple, list)) and len(ring) == 3:
        return ring
    elif hasattr(ring, 'elements') and hasattr(ring, 'add') and hasattr(ring, 'mul'):
        return ring.elements, ring.add, ring.mul
    elif isinstance(ring, dict) and 'elements' in ring:
        return ring['elements'], ring['add'], ring['mul']
    else:
        raise ValueError("Cannot parse ring")

def get_elements_list(elements):
    if isinstance(elements, (set, frozenset)):
        try:
            return sorted(list(elements))
        except Exception:
            return list(elements)
    else:
        E = []
        for e in elements:
            if e not in E:
                E.append(e)
        return E

def apply_op(op, x, y, elements_list):
    if callable(op):
        return op(x, y)
    elif isinstance(op, dict):
        if (x, y) in op: return op[(x, y)]
        if str((x, y)) in op: return op[str((x, y))]
    elif isinstance(op, (list, tuple)):
        if len(op) > 0 and isinstance(op[0], (list, tuple)) and len(op[0]) == 3:
            for triple in op:
                if triple[0] == x and triple[1] == y: return triple[2]
        try:
            i = elements_list.index(x)
            j = elements_list.index(y)
            return op[i][j]
        except (ValueError, IndexError, TypeError):
            pass
    raise ValueError(f"Cannot apply operation to {x}, {y}")

def apply_f(f, x, elements_list):
    if callable(f):
        return f(x)
    elif isinstance(f, dict):
        if x in f: return f[x]
        if str(x) in f: return f[str(x)]
    elif isinstance(f, (list, tuple)):
        if len(f) > 0 and isinstance(f[0], (list, tuple)) and len(f[0]) == 2:
            for pair in f:
                if pair[0] == x: return pair[1]
        try:
            i = elements_list.index(x)
            return f[i]
        except (ValueError, IndexError, TypeError):
            pass
    raise ValueError(f"Cannot apply function to {x}")

def is_commutative_ring_with_identity(ring_data):
    elements, add, mul = ring_data
    E = get_elements_list(elements)
        
    for x in E:
        for y in E:
            if apply_op(add, x, y, E) not in E: return False
            if apply_op(mul, x, y, E) not in E: return False

    zero = None
    for e in E:
        if all(apply_op(add, e, x, E) == x and apply_op(add, x, e, E) == x for x in E):
            zero = e
            break
    if zero is None: return False
    
    for x in E:
        if not any(apply_op(add, x, y, E) == zero and apply_op(add, y, x, E) == zero for y in E):
            return False
            
    for x in E:
        for y in E:
            xy_add = apply_op(add, x, y, E)
            yx_add = apply_op(add, y, x, E)
            if xy_add != yx_add: return False
            
            xy_mul = apply_op(mul, x, y, E)
            yx_mul = apply_op(mul, y, x, E)
            if xy_mul != yx_mul: return False
            
            for z in E:
                yz_add = apply_op(add, y, z, E)
                if apply_op(add, x, yz_add, E) != apply_op(add, xy_add, z, E): return False
                
                yz_mul = apply_op(mul, y, z, E)
                if apply_op(mul, x, yz_mul, E) != apply_op(mul, xy_mul, z, E): return False
                
                xz_mul = apply_op(mul, x, z, E)
                if apply_op(mul, x, yz_add, E) != apply_op(add, xy_mul, xz_mul, E): return False
                
    one = None
    for e in E:
        if all(apply_op(mul, e, x, E) == x and apply_op(mul, x, e, E) == x for x in E):
            one = e
            break
    if one is None: return False
    
    return True

def is_local_ring(ring_data):
    elements, add, mul = ring_data
    E = get_elements_list(elements)
        
    zero = None
    for e in E:
        if all(apply_op(add, e, x, E) == x for x in E):
            zero = e
            break
    if zero is None: return False
    
    one = None
    for e in E:
        if all(apply_op(mul, e, x, E) == x and apply_op(mul, x, e, E) == x for x in E):
            one = e
            break
    if one is None: return False
    if one == zero: return False
    
    non_units = []
    for x in E:
        is_unit = False
        for y in E:
            if apply_op(mul, x, y, E) == one and apply_op(mul, y, x, E) == one:
                is_unit = True
                break
        if not is_unit:
            non_units.append(x)
            
    for x in non_units:
        for y in non_units:
            if apply_op(add, x, y, E) not in non_units:
                return False
                
    for x in non_units:
        for r in E:
            if apply_op(mul, r, x, E) not in non_units:
                return False
            if apply_op(mul, x, r, E) not in non_units:
                return False
                
    return True

def is_zero_ring(ring_data):
    elements, add, mul = ring_data
    return len(get_elements_list(elements)) == 1

def is_surjective_homomorphism(R_data, S_data, f):
    R_elems, R_add, R_mul = R_data
    S_elems, S_add, S_mul = S_data
    
    RE = get_elements_list(R_elems)
    SE = get_elements_list(S_elems)
    
    image = []
    for r in RE:
        s = apply_f(f, r, RE)
        if s not in SE:
            return False
        if s not in image:
            image.append(s)
            
    if len(image) != len(SE):
        return False
        
    for x in RE:
        for y in RE:
            fx = apply_f(f, x, RE)
            fy = apply_f(f, y, RE)
            
            xy_add = apply_op(R_add, x, y, RE)
            f_xy_add = apply_f(f, xy_add, RE)
            if f_xy_add != apply_op(S_add, fx, fy, SE): return False
            
            xy_mul = apply_op(R_mul, x, y, RE)
            f_xy_mul = apply_f(f, xy_mul, RE)
            if f_xy_mul != apply_op(S_mul, fx, fy, SE): return False
            
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            S = witness.get("S")
            f = witness.get("f")
        else:
            R = witness.R
            S = witness.S
            f = witness.f
            
        R_data = get_ring_data(R)
        S_data = get_ring_data(S)
    except Exception:
        return [False, False, False, False, False]
        
    try:
        h1 = is_commutative_ring_with_identity(R_data)
    except Exception:
        h1 = False
        
    try:
        h2 = is_local_ring(R_data)
    except Exception:
        h2 = False
        
    try:
        h3 = not is_zero_ring(S_data)
    except Exception:
        h3 = False
        
    try:
        h4 = is_surjective_homomorphism(R_data, S_data, f)
    except Exception:
        h4 = False
        
    try:
        neg_q = not is_local_ring(S_data)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a local ring",
    "H_3: S is not the zero ring",
    "H_4: f is a surjective ring homomorphism from R to S",
    "¬Q: S is not a local ring"
]

N_HYP = 4
NEG_Q_INDEX = 4