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

def extract_ring(witness):
    if witness == 0 or witness == [0]:
        return 1, [[0]], [[0]]
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            n, add_table, mul_table = witness
            if isinstance(n, int) and isinstance(add_table, list) and isinstance(mul_table, list):
                return n, add_table, mul_table
        if hasattr(witness, 'n') and hasattr(witness, 'add_table') and hasattr(witness, 'mul_table'):
            return witness.n, witness.add_table, witness.mul_table
    except Exception:
        pass
    return None, None, None

def is_ring(n, add_table, mul_table):
    if len(add_table) != n or any(len(row) != n for row in add_table): return False
    if len(mul_table) != n or any(len(row) != n for row in mul_table): return False
    
    for i in range(n):
        for j in range(n):
            if not (isinstance(add_table[i][j], int) and 0 <= add_table[i][j] < n): return False
            if not (isinstance(mul_table[i][j], int) and 0 <= mul_table[i][j] < n): return False
            
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False
    
    for i in range(n):
        if not any(add_table[i][j] == zero for j in range(n)): return False
        
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False
                
    return True

def is_boolean_ring(n, add_table, mul_table):
    if not is_ring(n, add_table, mul_table): return False
    for i in range(n):
        if mul_table[i][i] != i: return False
    return True

def has_mult_identity(n, add_table, mul_table):
    for i in range(n):
        if all(mul_table[i][j] == j and mul_table[j][i] == j for j in range(n)):
            return True
    return False

def get_ideals(n, add_table, mul_table, zero):
    ideals = set()
    ideals.add(frozenset([zero]))
    
    principal_ideals = []
    for i in range(n):
        closure = set([zero, i])
        while True:
            new_elements = set(closure)
            for x in closure:
                for y in closure:
                    new_elements.add(add_table[x][y])
            for x in closure:
                for r in range(n):
                    new_elements.add(mul_table[r][x])
                    new_elements.add(mul_table[x][r])
            if len(new_elements) == len(closure):
                break
            closure = new_elements
        ideals.add(frozenset(closure))
        
    principal_ideals = list(ideals)
    current_ideals = set(principal_ideals)
    while True:
        new_ideals = set(current_ideals)
        for I1 in current_ideals:
            for I2 in principal_ideals:
                sum_ideal = frozenset(add_table[x][y] for x in I1 for y in I2)
                new_ideals.add(sum_ideal)
        if len(new_ideals) == len(current_ideals):
            break
        current_ideals = new_ideals
        
    return current_ideals

def get_prime_ideals(n, mul_table, ideals):
    prime_ideals = []
    full_set = frozenset(range(n))
    for I in ideals:
        if I == full_set:
            continue
        is_prime = True
        for a in range(n):
            if a in I: continue
            for b in range(n):
                if b in I: continue
                if mul_table[a][b] in I:
                    is_prime = False
                    break
            if not is_prime:
                break
        if is_prime:
            prime_ideals.append(I)
    return prime_ideals

def get_krull_dimension(prime_ideals):
    if not prime_ideals:
        return -1
    
    prime_ideals = sorted(prime_ideals, key=len)
    depths = {I: 0 for I in prime_ideals}
    
    for i in range(len(prime_ideals)):
        I = prime_ideals[i]
        for j in range(i):
            J = prime_ideals[j]
            if J < I:
                if depths[J] + 1 > depths[I]:
                    depths[I] = depths[J] + 1
                    
    return max(depths.values())

def conditions(witness):
    n, add_table, mul_table = extract_ring(witness)
    if n is None:
        return [False, False, False]
        
    try:
        h1 = is_boolean_ring(n, add_table, mul_table)
    except Exception:
        h1 = False
        
    try:
        h2 = has_mult_identity(n, add_table, mul_table)
    except Exception:
        h2 = False
        
    try:
        if not is_ring(n, add_table, mul_table):
            neg_q = False
        else:
            zero = None
            for i in range(n):
                if all(add_table[i][j] == j for j in range(n)):
                    zero = i
                    break
            ideals = get_ideals(n, add_table, mul_table, zero)
            prime_ideals = get_prime_ideals(n, mul_table, ideals)
            kd = get_krull_dimension(prime_ideals)
            neg_q = (kd != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has a multiplicative identity 1",
    "¬Q: The Krull dimension of R is not 0"
]

N_HYP = 2
NEG_Q_INDEX = 2