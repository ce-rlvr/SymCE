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

def parse_witness(witness):
    """
    Accepts either:
    - (n, P) where n is an int (representing Z_n) and P is a list of elements.
    - (R_elements, add_func, mult_func, P) for an arbitrary finite ring.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        n, P = witness
        if isinstance(n, int) and n > 0:
            R_elements = list(range(n))
            add = lambda a, b: (a + b) % n
            mult = lambda a, b: (a * b) % n
            return R_elements, add, mult, P
    elif isinstance(witness, tuple) and len(witness) == 4:
        return witness
    raise ValueError("Invalid witness format")

def get_zero(R_elements, add):
    for z in R_elements:
        if all(add(z, a) == a and add(a, z) == a for a in R_elements):
            return z
    return None

def is_comm_ring_with_id(R_elements, add, mult):
    if not R_elements: return False
    
    # check closure
    for a in R_elements:
        for b in R_elements:
            try:
                if add(a, b) not in R_elements: return False
                if mult(a, b) not in R_elements: return False
            except Exception:
                return False
                
    # check add commutativity
    for a in R_elements:
        for b in R_elements:
            if add(a, b) != add(b, a): return False
            
    # check add associativity
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    # check zero
    z = get_zero(R_elements, add)
    if z is None: return False
    
    # check add inverse
    for a in R_elements:
        has_inv = False
        for b in R_elements:
            if add(a, b) == z:
                has_inv = True
                break
        if not has_inv: return False
        
    # check mult associativity
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                if mult(mult(a, b), c) != mult(a, mult(b, c)): return False
                
    # check mult commutativity
    for a in R_elements:
        for b in R_elements:
            if mult(a, b) != mult(b, a): return False
            
    # check distributivity
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                if mult(a, add(b, c)) != add(mult(a, b), mult(a, c)): return False
                
    # check identity
    has_id = False
    for e in R_elements:
        if all(mult(e, a) == a and mult(a, e) == a for a in R_elements):
            has_id = True
            break
    if not has_id: return False
    
    return True

def get_all_ideals(R_elements, add, mult, zero):
    def ideal_generated_by(generators):
        I = set(generators)
        if not I:
            return frozenset({zero})
        while True:
            new_I = set(I)
            for a in I:
                for b in I:
                    new_I.add(add(a, b))
            for a in I:
                for r in R_elements:
                    new_I.add(mult(r, a))
                    new_I.add(mult(a, r))
            for a in I:
                for x in R_elements:
                    if add(a, x) == zero:
                        new_I.add(x)
                        break
            if len(new_I) == len(I):
                break
            I = new_I
        return frozenset(I)

    principal_ideals = set()
    for a in R_elements:
        principal_ideals.add(ideal_generated_by([a]))
    
    all_ideals = set(principal_ideals)
    queue = list(principal_ideals)
    
    while queue:
        current = queue.pop(0)
        for p in principal_ideals:
            combined = ideal_generated_by(list(current) + list(p))
            if combined not in all_ideals:
                all_ideals.add(combined)
                queue.append(combined)
                
    return [list(I) for I in all_ideals]

def is_prime_ideal(R_elements, add, mult, zero, I):
    if set(I) == set(R_elements):
        return False
    for a in R_elements:
        for b in R_elements:
            if mult(a, b) in I:
                if a not in I and b not in I:
                    return False
    return True

def get_prime_ideals(R_elements, add, mult, zero, all_ideals):
    prime_ideals = []
    for I in all_ideals:
        if is_prime_ideal(R_elements, add, mult, zero, I):
            prime_ideals.append(I)
    return prime_ideals

def get_minimal_prime_ideals(prime_ideals):
    minimal = []
    for I in prime_ideals:
        is_min = True
        for J in prime_ideals:
            if set(J) < set(I):
                is_min = False
                break
        if is_min:
            minimal.append(I)
    return minimal

def conditions(witness):
    try:
        R_elements, add, mult, P = parse_witness(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_comm_ring_with_id(R_elements, add, mult)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            zero = get_zero(R_elements, add)
            all_ideals = get_all_ideals(R_elements, add, mult, zero)
            prime_ideals = get_prime_ideals(R_elements, add, mult, zero, all_ideals)
            min_primes = get_minimal_prime_ideals(prime_ideals)
            
            exists = False
            for Q in min_primes:
                if set(Q).issubset(set(P)):
                    exists = True
                    break
            neg_q = not exists
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: There does not exist a minimal prime ideal Q of R such that Q is a subset of P"
]

N_HYP = 1
NEG_Q_INDEX = 1