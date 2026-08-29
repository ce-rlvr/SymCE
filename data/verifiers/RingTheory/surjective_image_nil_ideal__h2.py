import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Expected witness format:
# A tuple or dict containing:
# R_add: n x n list of lists for R's addition table
# R_mul: n x n list of lists for R's multiplication table
# S_add: m x m list of lists for S's addition table
# S_mul: m x m list of lists for S's multiplication table
# I: list of integers representing the ideal in R
# f: list, dict, or callable mapping R's elements (0 to n-1) to S's elements (0 to m-1)

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

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: I is a nil ideal of R",
    "¬Q: The image f(I) is not a nil ideal of S"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_zero(add):
    n = len(add)
    for e in range(n):
        if all(add[i][e] == i and add[e][i] == i for i in range(n)):
            return e
    return None

def is_commutative_ring(add, mul):
    try:
        n = len(add)
        if n == 0: return False
        if len(mul) != n: return False
        for row in add + mul:
            if len(row) != n: return False
            for x in row:
                if not isinstance(x, int): return False
                if not (0 <= x < n): return False
                
        # Additive identity
        zero = get_zero(add)
        if zero is None: return False
                
        # Additive inverse
        for i in range(n):
            if not any(add[i][j] == zero and add[j][i] == zero for j in range(n)):
                return False
                
        # Commutativity of add and mul
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: return False
                if mul[i][j] != mul[j][i]: return False
                
        # Associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                    # Distributivity
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                    
        # Multiplicative identity
        has_id = False
        for e in range(n):
            if all(mul[i][e] == i and mul[e][i] == i for i in range(n)):
                has_id = True
                break
        if not has_id: return False
        
        return True
    except Exception:
        return False

def is_ideal(add, mul, I):
    try:
        if not I: return False
        n = len(add)
        zero = get_zero(add)
        if zero is None: return False
        
        for x in I:
            if not isinstance(x, int) or not (0 <= x < n):
                return False
                
        I_set = set(I)
        if zero not in I_set: return False
        
        # I must be closed under addition
        for x in I_set:
            for y in I_set:
                if add[x][y] not in I_set: return False
        # I must be closed under additive inverse
        for x in I_set:
            inv_x = next((y for y in range(n) if add[x][y] == zero), None)
            if inv_x is None or inv_x not in I_set: return False
        # I must absorb multiplication from R
        for x in I_set:
            for r in range(n):
                if mul[x][r] not in I_set: return False
                if mul[r][x] not in I_set: return False
        return True
    except Exception:
        return False

def is_nil_ideal(add, mul, I):
    try:
        if not is_ideal(add, mul, I): return False
        n = len(add)
        zero = get_zero(add)
        
        # Every element in I must be nilpotent
        for x in I:
            curr = x
            is_nil = False
            for _ in range(n + 1):
                if curr == zero:
                    is_nil = True
                    break
                curr = mul[curr][x]
            if not is_nil: return False
        return True
    except Exception:
        return False

def is_valid_function(f, n, m):
    try:
        if callable(f):
            for i in range(n):
                val = f(i)
                if not isinstance(val, int) or not (0 <= val < m):
                    return False
            return True
        elif isinstance(f, dict):
            if len(f) != n: return False
            for i in range(n):
                if i not in f: return False
                val = f[i]
                if not isinstance(val, int) or not (0 <= val < m):
                    return False
            return True
        elif isinstance(f, (list, tuple)):
            if len(f) != n: return False
            for x in f:
                if not isinstance(x, int) or not (0 <= x < m):
                    return False
            return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            I = witness['I']
            f = witness['f']
        else:
            R_add, R_mul, S_add, S_mul, I, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring(R_add, R_mul) and is_commutative_ring(S_add, S_mul)
    except Exception:
        h1 = False
        
    try:
        h2 = is_nil_ideal(R_add, R_mul, I)
    except Exception:
        h2 = False
        
    try:
        n = len(R_add)
        m = len(S_add)
        if not is_valid_function(f, n, m):
            neg_q = False
        else:
            if callable(f):
                f_I = list(set(f(x) for x in I))
            else:
                f_I = list(set(f[x] for x in I))
            neg_q = not is_nil_ideal(S_add, S_mul, f_I)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]