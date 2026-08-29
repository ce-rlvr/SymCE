import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: q_1, ..., q_k are primary ideals of R",
    "H_3: The radical \\sqrt{q_i} equals P for all i from 1 to k",
    "¬Q: The intersection q_1 \\cap ... \\cap q_k is NOT a primary ideal OR its radical is NOT P"
]

N_HYP = 3
NEG_Q_INDEX = 3

def unpack_witness(witness):
    # Support for a simple Z/nZ witness: (n, q_list, P)
    if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
        n, q_list, P = witness
        if n <= 0:
            raise ValueError("n must be positive")
        elements = list(range(n))
        add_table = {i: {j: (i + j) % n for j in range(n)} for i in range(n)}
        mul_table = {i: {j: (i * j) % n for j in range(n)} for i in range(n)}
        zero = 0
        one = 1 % n
        return elements, add_table, mul_table, zero, one, q_list, P
    
    # Support for explicit finite ring dictionary or object
    if isinstance(witness, dict):
        elements = witness['elements']
        add = witness['add']
        mul = witness['mul']
        zero = witness['zero']
        one = witness['one']
        q_list = witness['q_list']
        P = witness['P']
    elif isinstance(witness, tuple) and len(witness) == 7:
        elements, add, mul, zero, one, q_list, P = witness
    else:
        elements = witness.elements
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        one = witness.one
        q_list = witness.q_list
        P = witness.P

    # Normalize add and mul to dict of dicts
    if callable(add):
        add_table = {a: {b: add(a, b) for b in elements} for a in elements}
    elif isinstance(add, list):
        add_table = {elements[i]: {elements[j]: add[i][j] for j in range(len(elements))} for i in range(len(elements))}
    else:
        add_table = add

    if callable(mul):
        mul_table = {a: {b: mul(a, b) for b in elements} for a in elements}
    elif isinstance(mul, list):
        mul_table = {elements[i]: {elements[j]: mul[i][j] for j in range(len(elements))} for i in range(len(elements))}
    else:
        mul_table = mul

    return elements, add_table, mul_table, zero, one, q_list, P

def check_H1(elements, add, mul, zero, one):
    if not elements: 
        return False
    if zero not in elements or one not in elements: 
        return False
    elements_set = set(elements)
    
    for a in elements:
        for b in elements:
            if add[a][b] not in elements_set: return False
            if mul[a][b] not in elements_set: return False
            if add[a][b] != add[b][a]: return False
            if mul[a][b] != mul[b][a]: return False
            
    for a in elements:
        if add[a][zero] != a: return False
        if mul[a][one] != a: return False
        has_inv = False
        for b in elements:
            if add[a][b] == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in elements:
        for b in elements:
            for c in elements:
                if add[add[a][b]][c] != add[a][add[b][c]]: return False
                if mul[mul[a][b]][c] != mul[a][mul[b][c]]: return False
                if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]: return False
                
    return True

def is_ideal(elements, add, mul, zero, q):
    q_set = set(q)
    if not q_set.issubset(set(elements)): return False
    if zero not in q_set: return False
    
    for a in q_set:
        for b in q_set:
            if add[a][b] not in q_set: return False
            inv_a = None
            for x in elements:
                if add[a][x] == zero:
                    inv_a = x
                    break
            if inv_a not in q_set: return False
            
    for a in q_set:
        for r in elements:
            if mul[r][a] not in q_set: return False
            if mul[a][r] not in q_set: return False
            
    return True

def get_radical(elements, mul, q):
    rad = set()
    q_set = set(q)
    n = len(set(elements))
    for x in elements:
        curr = x
        for _ in range(n + 1):
            if curr in q_set:
                rad.add(x)
                break
            curr = mul[curr][x]
    return rad

def check_primary(elements, mul, q, rad_q):
    q_set = set(q)
    if len(q_set) == len(set(elements)): 
        return False # A primary ideal must be proper
        
    for x in elements:
        for y in elements:
            if mul[x][y] in q_set:
                if x not in q_set and y not in rad_q:
                    return False
    return True

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero, one, q_list, P = unpack_witness(witness)
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = check_H1(elements, add, mul, zero, one)
    except Exception:
        h1 = False

    try:
        h2 = True
        for q in q_list:
            if not is_ideal(elements, add, mul, zero, q):
                h2 = False
                break
            rad_q = get_radical(elements, mul, q)
            if not check_primary(elements, mul, q, rad_q):
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        h3 = True
        P_set = set(P)
        if not is_ideal(elements, add, mul, zero, P):
            h3 = False
        else:
            for q in q_list:
                rad_q = get_radical(elements, mul, q)
                if rad_q != P_set:
                    h3 = False
                    break
    except Exception:
        h3 = False

    try:
        if not q_list:
            inter = set(elements)
        else:
            inter = set(q_list[0])
            for q in q_list[1:]:
                inter = inter.intersection(set(q))
        
        is_inter_ideal = is_ideal(elements, add, mul, zero, list(inter))
        if not is_inter_ideal:
            q_holds = False
        else:
            rad_inter = get_radical(elements, mul, list(inter))
            is_inter_primary = check_primary(elements, mul, list(inter), rad_inter)
            q_holds = is_inter_primary and (rad_inter == set(P))
        
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]