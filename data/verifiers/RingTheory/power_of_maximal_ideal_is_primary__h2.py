import math
from itertools import product
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12
Z16 = 16
Z24 = 24
Z36 = 36

class RingWrapper:
    def __init__(self, R):
        self.R = R
        if isinstance(R, int):
            self.type = 'Zm'
            self.m = R
            self.elements = list(range(R))
        elif isinstance(R, tuple) and len(R) == 3:
            self.type = 'custom'
            self.elements = list(R[0])
            self.add_table = R[1]
            self.mul_table = R[2]
        else:
            raise ValueError("Unknown ring format")

    def add_op(self, a, b):
        if self.type == 'Zm':
            return (a + b) % self.m
        if isinstance(self.add_table, dict):
            return self.add_table[(a, b)]
        return self.add_table(a, b)

    def mul_op(self, a, b):
        if self.type == 'Zm':
            return (a * b) % self.m
        if isinstance(self.mul_table, dict):
            return self.mul_table[(a, b)]
        return self.mul_table(a, b)

    def is_commutative_ring(self):
        if self.type == 'Zm':
            return self.m > 1
        n_elem = len(self.elements)
        if n_elem == 0: return False
        
        for a in self.elements:
            for b in self.elements:
                if self.add_op(a, b) != self.add_op(b, a): return False
                if self.mul_op(a, b) != self.mul_op(b, a): return False
                
        if n_elem <= 50:
            for a in self.elements:
                for b in self.elements:
                    for c in self.elements:
                        if self.add_op(self.add_op(a, b), c) != self.add_op(a, self.add_op(b, c)): return False
                        if self.mul_op(self.mul_op(a, b), c) != self.mul_op(a, self.mul_op(b, c)): return False
            for a in self.elements:
                for b in self.elements:
                    for c in self.elements:
                        if self.mul_op(a, self.add_op(b, c)) != self.add_op(self.mul_op(a, b), self.mul_op(a, c)): return False
                        
        has_zero = False
        for z_elem in self.elements:
            is_z = True
            for a in self.elements:
                if self.add_op(z_elem, a) != a:
                    is_z = False
                    break
            if is_z:
                has_zero = True
                break
        if not has_zero: return False
        return True

def generate_ideal(ring, generators):
    if ring.type == 'Zm':
        g = ring.m
        for val in generators:
            g = math.gcd(g, val % ring.m)
        return set(i for i in range(ring.m) if i % g == 0)
        
    ideal = set()
    zero = None
    for val in ring.elements:
        if all(ring.add_op(val, y_elem) == y_elem for y_elem in ring.elements):
            zero = val
            break
    if zero is not None:
        ideal.add(zero)
        
    for g_elem in generators:
        for r in ring.elements:
            ideal.add(ring.mul_op(g_elem, r))
            
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for a in ideal:
            for b in ideal:
                s = ring.add_op(a, b)
                if s not in ideal:
                    new_elements.add(s)
        if new_elements:
            ideal.update(new_elements)
            changed = True
    return ideal

def get_ideal_elements(ring, M_input):
    if isinstance(M_input, int):
        generators = [M_input]
    elif isinstance(M_input, (list, set, tuple)):
        generators = list(M_input)
    else:
        raise ValueError("Unknown M format")
    return list(generate_ideal(ring, generators))

def is_ideal(ring, M_elements):
    if ring.type == 'Zm':
        if not M_elements: return False
        g = ring.m
        for val in M_elements:
            g = math.gcd(g, val)
        expected = set(i for i in range(ring.m) if i % g == 0)
        return set(M_elements) == expected

    M_set = set(M_elements)
    if not M_set: return False
    for a in M_set:
        for b in M_set:
            if ring.add_op(a, b) not in M_set: return False
    for a in M_set:
        for r in ring.elements:
            if ring.mul_op(a, r) not in M_set: return False
    return True

def multiply_ideals(ring, I1, I2):
    generators = set()
    for a in I1:
        for b in I2:
            generators.add(ring.mul_op(a, b))
    return generate_ideal(ring, generators)

def compute_power_ideal(ring, M_elements, n):
    if ring.type == 'Zm':
        g = ring.m
        for val in M_elements:
            g = math.gcd(g, val)
        gn = math.gcd(ring.m, g ** n)
        return set(i for i in range(ring.m) if i % gn == 0)

    if n == 1:
        return set(M_elements)
    result = set(M_elements)
    for _ in range(n - 1):
        result = multiply_ideals(ring, result, M_elements)
    return result

def compute_radical(ring, Q_elements):
    if ring.type == 'Zm':
        g = ring.m
        for val in Q_elements:
            g = math.gcd(g, val)
        temp = g
        rad_g = 1
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                rad_g *= d
                while temp % d == 0:
                    temp //= d
            d += 1
        if temp > 1:
            rad_g *= temp
        return set(i for i in range(ring.m) if i % rad_g == 0)

    rad = set()
    max_k = len(ring.elements)
    for val in ring.elements:
        curr = val
        if curr in Q_elements:
            rad.add(val)
            continue
        found = False
        for k in range(2, max_k + 1):
            curr = ring.mul_op(curr, val)
            if curr in Q_elements:
                found = True
                break
        if found:
            rad.add(val)
    return rad

def is_M_primary(ring, Q_elements, M_elements):
    if ring.type == 'Zm':
        g_Q = ring.m
        for val in Q_elements:
            g_Q = math.gcd(g_Q, val)
            
        g_M = ring.m
        for val in M_elements:
            g_M = math.gcd(g_M, val)
            
        temp = g_Q
        rad_g = 1
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                rad_g *= d
                while temp % d == 0:
                    temp //= d
            d += 1
        if temp > 1:
            rad_g *= temp
            
        if rad_g != g_M:
            return False
            
        if g_Q == 1:
            return False
        temp = g_Q
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                while temp % d == 0:
                    temp //= d
                return temp == 1
            d += 1
        return True

    rad_Q = compute_radical(ring, Q_elements)
    if set(rad_Q) != set(M_elements):
        return False
    
    for a in ring.elements:
        for b in ring.elements:
            if ring.mul_op(a, b) in Q_elements:
                if a not in Q_elements and b not in rad_Q:
                    return False
                    
    if len(Q_elements) == len(ring.elements):
        return False
        
    return True

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        R_input, M_input, n = witness
    except Exception:
        return [False, False, False]
    
    try:
        ring = RingWrapper(R_input)
        h1 = ring.is_commutative_ring()
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    try:
        M_elements = get_ideal_elements(ring, M_input)
        if not is_ideal(ring, M_elements):
            neg_q = False
        else:
            Mn_elements = compute_power_ideal(ring, M_elements, n)
            is_M_prim = is_M_primary(ring, Mn_elements, M_elements)
            neg_q = not is_M_prim
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a positive integer",
    "¬Q: The ideal M^n is not an M-primary ideal"
]
N_HYP = 2
NEG_Q_INDEX = 2