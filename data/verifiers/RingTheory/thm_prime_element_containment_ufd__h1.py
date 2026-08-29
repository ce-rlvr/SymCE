import sympy
from sympy import Symbol, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math
import z3

# Top-level setup
# Expected witness format:
# A dictionary or object representing a finite commutative ring:
# {
#   'n': int, # number of elements (<= 100)
#   'add': [[int]], # n x n addition table (or callable)
#   'mul': [[int]], # n x n multiplication table (or callable)
#   'zero': int, # additive identity
#   'one': int, # multiplicative identity
#   'P': [int] # list of elements in the prime ideal
# }

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            add_table = witness.get('add')
            mul_table = witness.get('mul')
            zero = witness.get('zero')
            one = witness.get('one')
            P = witness.get('P')
        else:
            n = getattr(witness, 'n', None)
            add_table = getattr(witness, 'add', None)
            mul_table = getattr(witness, 'mul', None)
            zero = getattr(witness, 'zero', None)
            one = getattr(witness, 'one', None)
            P = getattr(witness, 'P', None)
            
        if n is None or add_table is None or mul_table is None or zero is None or one is None or P is None:
            return [False, False, False]
            
        if not (isinstance(n, int) and 0 < n <= 100): 
            return [False, False, False]
            
        if callable(add_table):
            add = [[add_table(i, j) for j in range(n)] for i in range(n)]
        else:
            add = add_table
            
        if callable(mul_table):
            mul = [[mul_table(i, j) for j in range(n)] for i in range(n)]
        else:
            mul = mul_table
            
        if zero not in range(n) or one not in range(n): 
            return [False, False, False]
        if zero == one: 
            return [False, False, False]
        
        if len(add) != n or any(len(row) != n for row in add): 
            return [False, False, False]
        if len(mul) != n or any(len(row) != n for row in mul): 
            return [False, False, False]
        
        for row in add:
            if any(val not in range(n) for val in row): return [False, False, False]
        for row in mul:
            if any(val not in range(n) for val in row): return [False, False, False]
        
        # Check commutative ring axioms
        for a in range(n):
            for b in range(n):
                if add[a][b] != add[b][a]: return [False, False, False]
                if mul[a][b] != mul[b][a]: return [False, False, False]
                for c in range(n):
                    if add[add[a][b]][c] != add[a][add[b][c]]: return [False, False, False]
                    if mul[mul[a][b]][c] != mul[a][mul[b][c]]: return [False, False, False]
                    if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]: return [False, False, False]
            if add[a][zero] != a: return [False, False, False]
            if mul[a][one] != a: return [False, False, False]
            
            has_inv = False
            for b in range(n):
                if add[a][b] == zero:
                    has_inv = True
                    break
            if not has_inv: return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H1: P is a prime ideal of R
    try:
        P_set = set(P)
        if not P_set.issubset(set(range(n))):
            h1 = False
        elif len(P_set) == 0:
            h1 = False
        elif len(P_set) == n:
            h1 = False
        else:
            is_ideal = True
            for a in P_set:
                for b in P_set:
                    if add[a][b] not in P_set:
                        is_ideal = False
                for r in range(n):
                    if mul[a][r] not in P_set:
                        is_ideal = False
            
            is_prime = True
            for a in range(n):
                for b in range(n):
                    if mul[a][b] in P_set:
                        if a not in P_set and b not in P_set:
                            is_prime = False
            
            h1 = is_ideal and is_prime
    except Exception:
        h1 = False

    # H2: P is not the zero ideal
    try:
        h2 = any(x_val != zero for x_val in P_set)
    except Exception:
        h2 = False

    # neg_Q: P contains no prime element of R
    try:
        units = set()
        for a in range(n):
            for b in range(n):
                if mul[a][b] == one:
                    units.add(a)
                    
        def is_prime_element(p):
            if p == zero: return False
            if p in units: return False
            
            I_p = set(mul[p][r] for r in range(n))
            
            for a in range(n):
                for b in range(n):
                    if mul[a][b] in I_p:
                        if a not in I_p and b not in I_p:
                            return False
            return True
            
        contains_prime = any(is_prime_element(p) for p in P_set)
        neg_q = not contains_prime
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: P is not the zero ideal",
    "¬Q: P contains no prime element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2