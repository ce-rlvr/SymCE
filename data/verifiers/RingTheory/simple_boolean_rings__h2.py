import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
Z2 = (2,
      [[(i + j) % 2 for j in range(2)] for i in range(2)],
      [[(i * j) % 2 for j in range(2)] for i in range(2)])

Z2xZ2 = (4, 
         [[(i ^ j) for j in range(4)] for i in range(4)], 
         [[(i & j) for j in range(4)] for i in range(4)])

PowerSet2 = [set(), {1}, {2}, {1, 2}]

def parse_witness(witness):
    try:
        if isinstance(witness, str):
            if witness.lower() in ["z2xz2", "z2 x z2"]:
                return Z2xZ2
            if witness.lower() == "z2":
                return Z2
        if isinstance(witness, int):
            n = witness
            add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
            mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
            return (n, add_table, mul_table)
        if isinstance(witness, list) and all(isinstance(x, (set, frozenset)) for x in witness):
            n = len(witness)
            add_table = [[0] * n for _ in range(n)]
            mul_table = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    add_res = set(witness[i]).symmetric_difference(set(witness[j]))
                    mul_res = set(witness[i]).intersection(set(witness[j]))
                    add_idx = -1
                    mul_idx = -1
                    for k, w in enumerate(witness):
                        if set(w) == add_res: add_idx = k
                        if set(w) == mul_res: mul_idx = k
                    if add_idx == -1 or mul_idx == -1:
                        return None
                    add_table[i][j] = add_idx
                    mul_table[i][j] = mul_idx
            return (n, add_table, mul_table)
        if isinstance(witness, tuple) and len(witness) == 3:
            n, add_table, mul_table = witness
            if isinstance(n, int) and isinstance(add_table, (list, tuple)) and isinstance(mul_table, (list, tuple)):
                return (n, add_table, mul_table)
            
            elements, add_op, mul_op = witness
            if isinstance(elements, (list, tuple)) and callable(add_op) and callable(mul_op):
                n = len(elements)
                add_table = [[0] * n for _ in range(n)]
                mul_table = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        a = add_op(elements[i], elements[j])
                        m = mul_op(elements[i], elements[j])
                        add_table[i][j] = elements.index(a)
                        mul_table[i][j] = elements.index(m)
                return (n, add_table, mul_table)
    except Exception:
        pass
    return None

def is_ring(n, add_table, mul_table):
    if n <= 0: return False
    if len(add_table) != n or any(len(row) != n for row in add_table): return False
    if len(mul_table) != n or any(len(row) != n for row in mul_table): return False
    
    for i in range(n):
        for j in range(n):
            if not (0 <= add_table[i][j] < n): return False
            if not (0 <= mul_table[i][j] < n): return False
            
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                
    zero = -1
    for e in range(n):
        if all(add_table[e][i] == i for i in range(n)):
            zero = e
            break
    if zero == -1: return False
    
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

def conditions(witness) -> list[bool]:
    parsed = parse_witness(witness)
    if parsed is None:
        return [False, False]
    
    n, add_table, mul_table = parsed
    
    try:
        h1 = is_boolean_ring(n, add_table, mul_table)
    except Exception:
        h1 = False
        
    try:
        is_z2 = False
        if n == 2:
            zero = -1
            for e in range(n):
                if all(add_table[e][i] == i for i in range(n)):
                    zero = e
                    break
            if zero != -1:
                one = 1 - zero
                if (mul_table[one][one] == one and 
                    mul_table[zero][one] == zero and 
                    mul_table[one][zero] == zero and 
                    mul_table[zero][zero] == zero):
                    is_z2 = True
        neg_q = not is_z2
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not isomorphic to Z2"
]

N_HYP = 1
NEG_Q_INDEX = 1