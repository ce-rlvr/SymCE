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

def is_commutative_ring(n, add, mul):
    if n <= 0: 
        return False
    for i in range(n):
        for j in range(n):
            if add[i][j] < 0 or add[i][j] >= n: return False
            if mul[i][j] < 0 or mul[i][j] >= n: return False
            if add[i][j] != add[j][i]: return False
            if mul[i][j] != mul[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[i][add[j][k]] != add[add[i][j]][k]: return False
                if mul[i][mul[j][k]] != mul[mul[i][j]][k]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                
    zero = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: 
        return False
    
    for i in range(n):
        has_inv = False
        for j in range(n):
            if add[i][j] == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        
    return True

def get_zero(n, add):
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            return i
    return None

def is_ideal(n, add, mul, zero, K):
    if not K: 
        return False
    if zero not in K: 
        return False
    for x in K:
        for y in K:
            inv_y = None
            for z in range(n):
                if add[y][z] == zero:
                    inv_y = z
                    break
            if inv_y is None: 
                return False
            if add[x][inv_y] not in K: 
                return False
    for x in K:
        for r in range(n):
            if mul[r][x] not in K: 
                return False
    return True

def is_regular(n, mul, zero, x):
    if x == zero: 
        return False
    for y in range(n):
        if y != zero and mul[x][y] == zero:
            return False
    return True

def contains_regular(n, mul, zero, K):
    for x in K:
        if is_regular(n, mul, zero, x):
            return True
    return False

def product_ideal(n, add, mul, zero, I, J):
    # If I or J is not an ideal, the product ideal is undefined/ill-typed.
    # We model this by returning an empty set, which contains no regular elements.
    if not is_ideal(n, add, mul, zero, I) or not is_ideal(n, add, mul, zero, J):
        return []
    
    closure = []
    for i in I:
        for j in J:
            p = mul[i][j]
            if p not in closure:
                closure.append(p)
                
    changed = True
    while changed:
        changed = False
        n_closure = len(closure)
        for i in range(n_closure):
            for j in range(n_closure):
                s = add[closure[i]][closure[j]]
                if s not in closure:
                    closure.append(s)
                    changed = True
                    
    changed = True
    while changed:
        changed = False
        n_closure = len(closure)
        for x in closure:
            for r in range(n):
                p = mul[r][x]
                if p not in closure:
                    closure.append(p)
                    changed = True
                    
    return closure

def conditions(witness):
    """
    witness is expected to be a tuple: (n, add, mul, I, J)
    where n is the size of the finite ring, add and mul are n x n lists of lists
    representing the addition and multiplication tables, and I and J are lists of elements.
    """
    try:
        n, add, mul, I, J = witness
        
        h1 = is_commutative_ring(n, add, mul)
        if not h1:
            return [False, False, False, False, False]
            
        zero = get_zero(n, add)
        
        h2 = is_ideal(n, add, mul, zero, J)
        h3 = contains_regular(n, mul, zero, I)
        h4 = contains_regular(n, mul, zero, J)
        
        IJ = product_ideal(n, add, mul, zero, I, J)
        neg_q = not contains_regular(n, mul, zero, IJ)
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "H_3: I contains at least one regular element",
    "H_4: J contains at least one regular element",
    "¬Q: The product ideal IJ does not contain at least one regular element"
]

N_HYP = 4
NEG_Q_INDEX = 4