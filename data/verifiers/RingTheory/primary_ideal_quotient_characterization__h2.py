import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    if isinstance(witness, tuple) and len(witness) == 2:
        n, m = witness
        if not (isinstance(n, int) and isinstance(m, int)):
            raise ValueError
        if n <= 0 or n > 100:
            raise ValueError
        elements = list(range(n))
        add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
        mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
        ideal_elements = []
        curr = 0
        for _ in range(n + 1):
            if curr not in ideal_elements:
                ideal_elements.append(curr)
            curr = (curr + m) % n
        return elements, add_table, mul_table, ideal_elements
    elif isinstance(witness, tuple) and len(witness) == 4:
        return witness
    else:
        raise ValueError

def is_commutative_ring(elements, add_table, mul_table):
    n = len(elements)
    if n == 0: return False
    
    if len(add_table) != n or any(len(row) != n for row in add_table): return False
    if len(mul_table) != n or any(len(row) != n for row in mul_table): return False
    
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)) and all(add_table[j][i] == j for j in range(n)):
            zero = i
            break
    if zero is None:
        return False
        
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False
            ij = add_table[i][j]
            for k in range(n):
                if add_table[ij][k] != add_table[i][add_table[j][k]]: return False
                
    for i in range(n):
        has_inv = False
        for j in range(n):
            if add_table[i][j] == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for i in range(n):
        for j in range(n):
            if mul_table[i][j] != mul_table[j][i]: return False
            ij = mul_table[i][j]
            for k in range(n):
                if mul_table[ij][k] != mul_table[i][mul_table[j][k]]: return False
                
    for i in range(n):
        for j in range(n):
            ij = mul_table[i][j]
            for k in range(n):
                if mul_table[i][add_table[j][k]] != add_table[ij][mul_table[i][k]]: return False
                
    return True

def is_ideal(elements, add_table, mul_table, ideal_elements):
    if not ideal_elements: return False
    n = len(elements)
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero not in ideal_elements: return False
    
    ideal_set = set(ideal_elements)
    for x in ideal_set:
        for y in ideal_set:
            if add_table[x][y] not in ideal_set: return False
            
    for x in ideal_set:
        inv_found = False
        for y in ideal_set:
            if add_table[x][y] == zero:
                inv_found = True
                break
        if not inv_found: return False
        
    for x in ideal_set:
        for r in range(n):
            if mul_table[r][x] not in ideal_set: return False
            if mul_table[x][r] not in ideal_set: return False
            
    return True

def get_quotient_ring(elements, add_table, mul_table, ideal_elements):
    n = len(elements)
    cosets = []
    element_to_coset = {}
    for i in range(n):
        if i in element_to_coset: continue
        coset = set()
        for x in ideal_elements:
            coset.add(add_table[i][x])
        coset_tuple = tuple(sorted(list(coset)))
        cosets.append(coset_tuple)
        for x in coset:
            element_to_coset[x] = cosets.index(coset_tuple)
            
    num_cosets = len(cosets)
    q_add = [[0]*num_cosets for _ in range(num_cosets)]
    q_mul = [[0]*num_cosets for _ in range(num_cosets)]
    
    for i in range(num_cosets):
        rep_i = cosets[i][0]
        for j in range(num_cosets):
            rep_j = cosets[j][0]
            sum_rep = add_table[rep_i][rep_j]
            prod_rep = mul_table[rep_i][rep_j]
            q_add[i][j] = element_to_coset[sum_rep]
            q_mul[i][j] = element_to_coset[prod_rep]
            
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    q_zero = element_to_coset[zero]
    
    return list(range(num_cosets)), q_add, q_mul, q_zero

def all_zd_nilpotent(q_elements, q_add, q_mul, q_zero):
    num_q = len(q_elements)
    if num_q == 1:
        return True
        
    zero_divisors = []
    for i in range(num_q):
        if i == q_zero: continue
        is_zd = False
        for j in range(num_q):
            if j == q_zero: continue
            if q_mul[i][j] == q_zero:
                is_zd = True
                break
        if is_zd:
            zero_divisors.append(i)
            
    for zd in zero_divisors:
        curr = zd
        is_nilpotent = False
        for _ in range(num_q + 1):
            if curr == q_zero:
                is_nilpotent = True
                break
            curr = q_mul[curr][zd]
        if not is_nilpotent:
            return False
            
    return True

def is_primary_ideal(elements, add_table, mul_table, ideal_elements):
    n = len(elements)
    if len(ideal_elements) == n:
        return False
        
    ideal_set = set(ideal_elements)
    for a in range(n):
        for b in range(n):
            prod = mul_table[a][b]
            if prod in ideal_set:
                if a in ideal_set:
                    continue
                curr = b
                b_nil_in_I = False
                for _ in range(n + 1):
                    if curr in ideal_set:
                        b_nil_in_I = True
                        break
                    curr = mul_table[curr][b]
                if not b_nil_in_I:
                    return False
    return True

def conditions(witness):
    try:
        elements, add_table, mul_table, ideal_elements = parse_witness(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_commutative_ring(elements, add_table, mul_table)
        if h1:
            h1 = is_ideal(elements, add_table, mul_table, ideal_elements)
    except Exception:
        h1 = False
        
    try:
        q_elements, q_add, q_mul, q_zero = get_quotient_ring(elements, add_table, mul_table, ideal_elements)
        lhs = is_primary_ideal(elements, add_table, mul_table, ideal_elements)
        rhs = all_zd_nilpotent(q_elements, q_add, q_mul, q_zero)
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: I is primary is not equivalent to every zero divisor in R/I being nilpotent"
]

N_HYP = 1
NEG_Q_INDEX = 1