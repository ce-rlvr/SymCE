import sympy
import itertools
import functools
import math

# Top-level setup: named object bindings
def make_boolean_ring(k):
    """
    Creates a Boolean ring isomorphic to (Z_2)^k.
    Returns a tuple (n, add_table, mul_table).
    """
    n = 2**k
    add_table = [[(i ^ j) for j in range(n)] for i in range(n)]
    mul_table = [[(i & j) for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

# Standard Boolean rings for use as witnesses
Z2 = make_boolean_ring(1)
Z2xZ2 = make_boolean_ring(2)
Z2xZ2xZ2 = make_boolean_ring(3)

def is_ring(n, add_table, mul_table):
    try:
        n = int(n)
    except Exception:
        return False
    if n <= 0:
        return False
    if len(add_table) != n or len(mul_table) != n:
        return False
    for row in add_table:
        if len(row) != n: return False
    for row in mul_table:
        if len(row) != n: return False
        
    for i in range(n):
        for j in range(n):
            try:
                add_val = int(add_table[i][j])
                mul_val = int(mul_table[i][j])
            except Exception:
                return False
            if not (0 <= add_val < n): return False
            if not (0 <= mul_val < n): return False

    # Addition commutativity
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False

    # Addition associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False

    # Additive identity
    zero = -1
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False

    # Additive inverses
    for i in range(n):
        if not any(add_table[i][j] == zero for j in range(n)): return False

    # Multiplication associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False

    # Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                if mul_table[add_table[j][k]][i] != add_table[mul_table[j][i]][mul_table[k][i]]: return False

    return True

def is_boolean_ring(n, add_table, mul_table):
    if not is_ring(n, add_table, mul_table): 
        return False
    # Boolean condition: x^2 = x
    for i in range(n):
        if mul_table[i][i] != i: 
            return False
    return True

def has_identity(n, add_table, mul_table):
    try:
        n = int(n)
    except Exception:
        return False
        
    zero = -1
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False
    
    one = -1
    for i in range(n):
        if all(mul_table[i][j] == j and mul_table[j][i] == j for j in range(n)):
            one = i
            break
    if one == -1: return False
    
    return one != zero

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'n') and hasattr(witness, 'add_table') and hasattr(witness, 'mul_table'):
            n = witness.n
            add_table = witness.add_table
            mul_table = witness.mul_table
        else:
            n, add_table, mul_table = witness
        n = int(n)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_boolean_ring(n, add_table, mul_table)
    except Exception:
        h1 = False
        
    try:
        h2 = has_identity(n, add_table, mul_table)
    except Exception:
        h2 = False
        
    try:
        # Any Boolean ring of size 2 is isomorphic to Z_2.
        # Thus, a finite Boolean ring is NOT isomorphic to Z_2 iff its size is not 2.
        neg_q = (n != 2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has an identity element 1 != 0",
    "¬Q: R is not isomorphic to Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2