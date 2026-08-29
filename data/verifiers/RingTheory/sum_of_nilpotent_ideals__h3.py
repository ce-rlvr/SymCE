import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_ring_ops(witness):
    """
    Parses the witness into ring operations and ideals.
    Accepts either a tuple (n, I, J) for Z/nZ, or a dictionary with explicit tables.
    """
    if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
        n, I, J = witness
        elements = list(range(n))
        add_table = { (i, j): (i+j)%n for i in elements for j in elements }
        mul_table = { (i, j): (i*j)%n for i in elements for j in elements }
        return elements, add_table, mul_table, 0, I, J
    elif isinstance(witness, dict):
        elements = witness["elements"]
        add_raw = witness["add"]
        mul_raw = witness["mul"]
        zero = witness["zero"]
        I = witness["I"]
        J = witness["J"]
        
        add_table = {}
        mul_table = {}
        if isinstance(add_raw, list):
            for i, a in enumerate(elements):
                for j, b in enumerate(elements):
                    add_table[(a, b)] = add_raw[i][j]
                    mul_table[(a, b)] = mul_raw[i][j]
        else:
            add_table = add_raw
            mul_table = mul_raw
            
        return elements, add_table, mul_table, zero, I, J
    else:
        raise ValueError("Unknown witness format")

def check_ring(elements, add_table, mul_table, zero):
    if zero not in elements: 
        return False
        
    # Check closure, commutativity for addition, and basic presence in tables
    for a in elements:
        for b in elements:
            if (a, b) not in add_table: return False
            if add_table[(a, b)] not in elements: return False
            if add_table[(a, b)] != add_table[(b, a)]: return False
            if (a, b) not in mul_table: return False
            if mul_table[(a, b)] not in elements: return False
            
    # Check identity and inverses for addition
    for a in elements:
        if add_table[(a, zero)] != a: return False
        has_inv = False
        for b in elements:
            if add_table[(a, b)] == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    # Check associativity and distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if add_table[(add_table[(a, b)], c)] != add_table[(a, add_table[(b, c)])]: return False
                if mul_table[(mul_table[(a, b)], c)] != mul_table[(a, mul_table[(b, c)])]: return False
                if mul_table[(a, add_table[(b, c)])] != add_table[(mul_table[(a, b)], mul_table[(a, c)])]: return False
                if mul_table[(add_table[(a, b)], c)] != add_table[(mul_table[(a, c)], mul_table[(b, c)])]: return False
                
    return True

def check_ideal(elements, add_table, mul_table, zero, I):
    if not I: return False
    if any(x not in elements for x in I): return False
    if zero not in I: return False
    
    # Closed under addition
    for a in I:
        for b in I:
            if add_table[(a, b)] not in I: return False
            
    # Absorbing under multiplication
    for r in elements:
        for i in I:
            if mul_table[(r, i)] not in I: return False
            if mul_table[(i, r)] not in I: return False
            
    return True

def ideal_mul(A, B, add_table, mul_table, zero):
    # The product of two ideals is the additive closure of the set of products
    prods = {mul_table[(a, b)] for a in A for b in B}
    res = list(prods)
    changed = True
    while changed:
        changed = False
        for x in res:
            for y in res:
                s = add_table[(x, y)]
                if s not in res:
                    res.append(s)
                    changed = True
    return res

def check_nilpotent(elements, add_table, mul_table, zero, I):
    if not I: return False
    curr = list(I)
    # A nilpotent ideal in a finite ring must vanish in at most |R| steps
    for _ in range(len(elements) + 1):
        if all(x == zero for x in curr):
            return True
        curr = ideal_mul(curr, I, add_table, mul_table, zero)
    return all(x == zero for x in curr)

def check_sum_ideal_nilpotent(elements, add_table, mul_table, zero, I, J):
    if not J or any(x not in elements for x in J):
        raise ValueError("J must be a non-empty subset of R")
        
    sum_set = set()
    for i in I:
        for j in J:
            sum_set.add(add_table[(i, j)])
    sum_ideal = list(sum_set)
    
    if not check_ideal(elements, add_table, mul_table, zero, sum_ideal):
        return False
        
    if not check_nilpotent(elements, add_table, mul_table, zero, sum_ideal):
        return False
        
    return True

def conditions(witness) -> list[bool]:
    try:
        elements, add_table, mul_table, zero, I, J = get_ring_ops(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_ring(elements, add_table, mul_table, zero)
    except Exception:
        h1 = False
        
    try:
        h2 = check_ideal(elements, add_table, mul_table, zero, I) and \
             check_nilpotent(elements, add_table, mul_table, zero, I)
    except Exception:
        h2 = False
        
    try:
        q = check_sum_ideal_nilpotent(elements, add_table, mul_table, zero, I, J)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is a nilpotent ideal of R",
    "¬Q: The sum ideal I + J is not a nilpotent ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2