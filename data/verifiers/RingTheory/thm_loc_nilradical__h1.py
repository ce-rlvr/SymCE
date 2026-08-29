import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def get_attr(obj, attr):
    if isinstance(obj, dict):
        return obj[attr]
    return getattr(obj, attr)

def parse_witness_H1(witness):
    if isinstance(witness, tuple):
        return witness[0], witness[1]
    R = get_attr(witness, 'R')
    S = get_attr(witness, 'S')
    return R, S

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) >= 4:
            return witness[0], witness[1], witness[2], witness[3]
        else:
            raise ValueError("Tuple must have at least 4 elements")
    R = get_attr(witness, 'R')
    S = get_attr(witness, 'S')
    S_inv_R = get_attr(witness, 'S_inv_R')
    loc_map = get_attr(witness, 'loc_map')
    return R, S, S_inv_R, loc_map

def get_elements(ring):
    if hasattr(ring, 'elements'):
        return ring.elements
    return list(ring)

def add(ring, a, b):
    if hasattr(ring, 'add'): return ring.add(a, b)
    return a + b

def mul(ring, a, b):
    if hasattr(ring, 'mul'): return ring.mul(a, b)
    return a * b

def eq(ring, a, b):
    if hasattr(ring, 'eq'): return ring.eq(a, b)
    return a == b

def get_zero(ring):
    if hasattr(ring, 'zero'): return ring.zero
    elements = get_elements(ring)
    for z in elements:
        if all(eq(ring, add(ring, x, z), x) for x in elements):
            return z
    return None

def get_one(ring):
    if hasattr(ring, 'one'): return ring.one
    elements = get_elements(ring)
    for e in elements:
        if all(eq(ring, mul(ring, x, e), x) and eq(ring, mul(ring, e, x), x) for x in elements):
            return e
    return None

def is_subset(R, S):
    elements = get_elements(R)
    for s in S:
        if not any(eq(R, s, r) for r in elements):
            return False
    return True

def is_mult_closed(R, S):
    if not S: 
        return False
    if not is_subset(R, S): 
        return False
    one = get_one(R)
    if one is not None and not any(eq(R, one, s) for s in S):
        return False
    for a in S:
        for b in S:
            c = mul(R, a, b)
            if not any(eq(R, c, s) for s in S):
                return False
    return True

def additive_closure(ring, base):
    closure = []
    for b in base:
        if not any(eq(ring, b, c) for c in closure):
            closure.append(b)
    
    i = 0
    while i < len(closure):
        for j in range(i + 1):
            c = add(ring, closure[i], closure[j])
            if not any(eq(ring, c, x) for x in closure):
                closure.append(c)
        i += 1
    return closure

def principal_ideal(ring, x):
    elements = get_elements(ring)
    base = []
    for r in elements:
        for s in elements:
            c = mul(ring, mul(ring, r, x), s)
            if not any(eq(ring, c, b) for b in base):
                base.append(c)
    return additive_closure(ring, base)

def ideal_mul(ring, I, J):
    base = []
    for x in I:
        for y in J:
            c = mul(ring, x, y)
            if not any(eq(ring, c, b) for b in base):
                base.append(c)
    return additive_closure(ring, base)

def is_nilpotent_ideal(ring, I):
    zero = get_zero(ring)
    if not I: 
        return True
    if len(I) == 1 and eq(ring, I[0], zero): 
        return True
    
    current = I
    max_power = len(get_elements(ring))
    for _ in range(max_power):
        current = ideal_mul(ring, current, I)
        if len(current) == 1 and eq(ring, current[0], zero):
            return True
    return False

def nilradical(ring):
    elements = get_elements(ring)
    N = []
    for x in elements:
        I_x = principal_ideal(ring, x)
        if is_nilpotent_ideal(ring, I_x):
            N.append(x)
    return N

def apply_map(loc_map, x, ring_R=None):
    if isinstance(loc_map, dict):
        try:
            return loc_map[x]
        except (TypeError, KeyError):
            for k, v in loc_map.items():
                if ring_R and eq(ring_R, k, x):
                    return v
                elif k == x:
                    return v
            raise KeyError("Element not found in loc_map")
    return loc_map(x)

def ideal_generated_by_subset(ring, subset):
    elements = get_elements(ring)
    base = []
    for x in subset:
        for r in elements:
            for s in elements:
                c = mul(ring, mul(ring, r, x), s)
                if not any(eq(ring, c, b) for b in base):
                    base.append(c)
    return additive_closure(ring, base)

def extension_of_ideal(R, S_inv_R, loc_map, I):
    image = []
    for x in I:
        img = apply_map(loc_map, x, R)
        image.append(img)
    return ideal_generated_by_subset(S_inv_R, image)

def ideals_equal(ring, I, J):
    if len(I) != len(J): 
        return False
    for x in I:
        if not any(eq(ring, x, y) for y in J):
            return False
    for y in J:
        if not any(eq(ring, y, x) for x in I):
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        R, S = parse_witness_H1(witness)
        H1 = is_mult_closed(R, S)
    except Exception:
        H1 = False

    try:
        R, S, S_inv_R, loc_map = parse_witness(witness)
        N_R = nilradical(R)
        N_S_inv_R = nilradical(S_inv_R)
        ext_N_R = extension_of_ideal(R, S_inv_R, loc_map, N_R)
        Q = ideals_equal(S_inv_R, N_S_inv_R, ext_N_R)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "¬Q: The nilradical of the localized ring S^{-1}R is not equal to the extension of the nilradical of R"
]

N_HYP = 1
NEG_Q_INDEX = 1