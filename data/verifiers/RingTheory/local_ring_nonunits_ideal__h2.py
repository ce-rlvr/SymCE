import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

class kZ_n:
    """
    Represents the ring kZ / nZ.
    """
    def __init__(self, k, n):
        self.k = k
        self.n = n
        self.elements = [(k * i) % n for i in range(n // math.gcd(k, n))]
        self.elements = list(set(self.elements))
        self.elements.sort()
        self.zero = 0

    def add(self, a, b):
        return (a + b) % self.n

    def mul(self, a, b):
        return (a * b) % self.n

    def __eq__(self, other):
        if not isinstance(other, kZ_n):
            return False
        return self.k == other.k and self.n == other.n

class CustomRing:
    """
    Represents a custom finite ring.
    """
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add_func = add_func
        self.mul_func = mul_func
        self.zero = zero
        
    def add(self, a, b):
        return self.add_func(a, b)
        
    def mul(self, a, b):
        return self.mul_func(a, b)

def is_commutative_ring(witness):
    if not hasattr(witness, 'elements') or not hasattr(witness, 'add') or not hasattr(witness, 'mul') or not hasattr(witness, 'zero'):
        return False
    elements = witness.elements
    if not isinstance(elements, list) and not isinstance(elements, tuple) and not isinstance(elements, set):
        return False
    elements = list(elements)
    if len(elements) == 0:
        return False
        
    z = witness.zero
    if z not in elements:
        return False
        
    # 0. Closure
    for a in elements:
        for b in elements:
            if witness.add(a, b) not in elements:
                return False
            if witness.mul(a, b) not in elements:
                return False
                
    # 1. Additive commutativity
    for a in elements:
        for b in elements:
            if witness.add(a, b) != witness.add(b, a):
                return False
                
    # 2. Additive associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if witness.add(witness.add(a, b), c) != witness.add(a, witness.add(b, c)):
                    return False
                    
    # 3. Zero element
    for a in elements:
        if witness.add(a, z) != a or witness.add(z, a) != a:
            return False
            
    # 4. Additive inverse
    for a in elements:
        has_inv = False
        for b in elements:
            if witness.add(a, b) == z and witness.add(b, a) == z:
                has_inv = True
                break
        if not has_inv:
            return False
            
    # 5. Multiplicative commutativity
    for a in elements:
        for b in elements:
            if witness.mul(a, b) != witness.mul(b, a):
                return False
                
    # 6. Multiplicative associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if witness.mul(witness.mul(a, b), c) != witness.mul(a, witness.mul(b, c)):
                    return False
                    
    # 7. Distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                left = witness.mul(a, witness.add(b, c))
                right = witness.add(witness.mul(a, b), witness.mul(a, c))
                if left != right:
                    return False
                left2 = witness.mul(witness.add(a, b), c)
                right2 = witness.add(witness.mul(a, c), witness.mul(b, c))
                if left2 != right2:
                    return False
                    
    return True

def get_all_ideals(witness):
    elements = list(witness.elements)
    n = len(elements)
    
    add_table = [[0]*n for _ in range(n)]
    mul_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            add_table[i][j] = elements.index(witness.add(elements[i], elements[j]))
            mul_table[i][j] = elements.index(witness.mul(elements[i], elements[j]))
            
    zero_idx = elements.index(witness.zero)
    
    inv_table = [0]*n
    for i in range(n):
        for j in range(n):
            if add_table[i][j] == zero_idx:
                inv_table[i] = j
                break
                
    ideals = set()
    ideals.add(frozenset([zero_idx]))
    
    principal_ideals = set()
    for x in range(n):
        ideal = set([x, zero_idx])
        added = True
        while added:
            added = False
            new_elements = set()
            for a in ideal:
                inv = inv_table[a]
                if inv not in ideal and inv not in new_elements:
                    new_elements.add(inv)
                for b in ideal:
                    s = add_table[a][b]
                    if s not in ideal and s not in new_elements:
                        new_elements.add(s)
                for r in range(n):
                    p1 = mul_table[r][a]
                    if p1 not in ideal and p1 not in new_elements:
                        new_elements.add(p1)
                    p2 = mul_table[a][r]
                    if p2 not in ideal and p2 not in new_elements:
                        new_elements.add(p2)
            if new_elements:
                ideal.update(new_elements)
                added = True
        principal_ideals.add(frozenset(ideal))
        
    ideals.update(principal_ideals)
    
    added = True
    while added:
        added = False
        new_ideals = set()
        for I1 in ideals:
            for I2 in principal_ideals:
                sum_ideal = set()
                for a in I1:
                    for b in I2:
                        sum_ideal.add(add_table[a][b])
                sum_ideal = frozenset(sum_ideal)
                if sum_ideal not in ideals and sum_ideal not in new_ideals:
                    new_ideals.add(sum_ideal)
        if new_ideals:
            ideals.update(new_ideals)
            added = True
            
    return ideals, zero_idx, n

def get_maximal_ideals(witness):
    ideals, zero_idx, n = get_all_ideals(witness)
    R_set = frozenset(range(n))
    proper_ideals = [I for I in ideals if I != R_set]
    maximal_ideals = []
    for I in proper_ideals:
        is_maximal = True
        for J in proper_ideals:
            if I != J and I.issubset(J):
                is_maximal = False
                break
        if is_maximal:
            maximal_ideals.append(I)
    return maximal_ideals

def is_local_ring(witness):
    max_ideals = get_maximal_ideals(witness)
    return len(max_ideals) == 1

def non_units_form_ideal(witness):
    elements = list(witness.elements)
    n = len(elements)
    
    add_table = [[0]*n for _ in range(n)]
    mul_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            add_table[i][j] = elements.index(witness.add(elements[i], elements[j]))
            mul_table[i][j] = elements.index(witness.mul(elements[i], elements[j]))
            
    zero_idx = elements.index(witness.zero)
    
    identity_idx = None
    for e in range(n):
        is_id = True
        for x in range(n):
            if mul_table[e][x] != x or mul_table[x][e] != x:
                is_id = False
                break
        if is_id:
            identity_idx = e
            break
            
    if identity_idx is None:
        units = set()
    else:
        units = set()
        for x in range(n):
            for y in range(n):
                if mul_table[x][y] == identity_idx and mul_table[y][x] == identity_idx:
                    units.add(x)
                    break
                    
    non_units = set(range(n)) - units
    
    if not non_units:
        return False
        
    if zero_idx not in non_units:
        return False
        
    for x in non_units:
        for y in non_units:
            if add_table[x][y] not in non_units:
                return False
                
    for x in non_units:
        for r in range(n):
            if mul_table[r][x] not in non_units:
                return False
            if mul_table[x][r] not in non_units:
                return False
                
    return True

def conditions(witness):
    try:
        h1 = is_commutative_ring(witness)
    except Exception:
        h1 = False
        
    try:
        local = is_local_ring(witness)
        non_units_ideal = non_units_form_ideal(witness)
        neg_q = (local != non_units_ideal)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The equivalence (R is local <=> non-units form an ideal) is false"
]

N_HYP = 1
NEG_Q_INDEX = 1