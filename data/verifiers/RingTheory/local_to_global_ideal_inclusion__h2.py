import itertools
import math
import functools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

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
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: The equivalence I \\subseteq J iff I_M \\subseteq J_M for all maximal ideals M fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_commutative_ring(n, add, mul):
    if not all(0 <= add[i][j] < n for i in range(n) for j in range(n)): return False
    if not all(add[i][j] == add[j][i] for i in range(n) for j in range(n)): return False
    if not all(add[add[i][j]][k] == add[i][add[j][k]] for i in range(n) for j in range(n) for k in range(n)): return False
    if not all(add[i][0] == i for i in range(n)): return False
    for i in range(n):
        if not any(add[i][j] == 0 for j in range(n)): return False
        
    if not all(0 <= mul[i][j] < n for i in range(n) for j in range(n)): return False
    if not all(mul[i][j] == mul[j][i] for i in range(n) for j in range(n)): return False
    if not all(mul[mul[i][j]][k] == mul[i][mul[j][k]] for i in range(n) for j in range(n) for k in range(n)): return False
    
    if not all(mul[i][add[j][k]] == add[mul[i][j]][mul[i][k]] for i in range(n) for j in range(n) for k in range(n)): return False
    
    return True

def is_ideal(n, add, mul, subset):
    if not subset: return False
    if 0 not in subset: return False
    for x in subset:
        for y in subset:
            if add[x][y] not in subset: return False
    for r in range(n):
        for x in subset:
            if mul[r][x] not in subset: return False
    return True

def get_all_ideals(n, add, mul):
    def generate_ideal(generators):
        closure = set(generators)
        closure.add(0)
        while True:
            old_len = len(closure)
            new_elements = set()
            for x in closure:
                for y in closure:
                    new_elements.add(add[x][y])
                for r in range(n):
                    new_elements.add(mul[r][x])
            closure.update(new_elements)
            if len(closure) == old_len:
                break
        return frozenset(closure)
        
    principal_ideals = set()
    for i in range(n):
        principal_ideals.add(generate_ideal([i]))
        
    all_ideals = set(principal_ideals)
    while True:
        old_len = len(all_ideals)
        new_ideals = set()
        for I1 in all_ideals:
            for I2 in all_ideals:
                sum_ideal = set()
                for x in I1:
                    for y in I2:
                        sum_ideal.add(add[x][y])
                new_ideals.add(frozenset(sum_ideal))
        all_ideals.update(new_ideals)
        if len(all_ideals) == old_len:
            break
    return [set(I) for I in all_ideals]

def get_maximal_ideals(n, add, mul):
    ideals = get_all_ideals(n, add, mul)
    proper_ideals = [I for I in ideals if len(I) < n]
    maximal_ideals = []
    for I in proper_ideals:
        is_max = True
        for J in proper_ideals:
            if I != J and I.issubset(J):
                is_max = False
                break
        if is_max:
            maximal_ideals.append(I)
    return maximal_ideals

def is_multiplicatively_closed(n, mul, S):
    for x in S:
        for y in S:
            if mul[x][y] not in S:
                return False
    return True

def check_IM_sub_JM(n, add, mul, neg, I, J, S):
    for i in I:
        for s in S:
            found_equiv = False
            for j in J:
                for t in S:
                    diff = add[mul[t][i]][neg[mul[s][j]]]
                    if any(mul[u][diff] == 0 for u in S):
                        found_equiv = True
                        break
                if found_equiv:
                    break
            if not found_equiv:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 5:
            return [False, False, False]
        n, add, mul, I_list, J_list = witness
        I = set(I_list)
        J = set(J_list)
        if not I.issubset(set(range(n))) or not J.issubset(set(range(n))):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_commutative_ring(n, add, mul)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_ideal(n, add, mul, J)
    except Exception:
        h2_ok = False
        
    try:
        if not h1_ok:
            neg_Q = False
        else:
            neg = [0]*n
            for x in range(n):
                for y in range(n):
                    if add[x][y] == 0:
                        neg[x] = y
                        break
                        
            I_sub_J = I.issubset(J)
            max_ideals = get_maximal_ideals(n, add, mul)
            
            rhs_true = True
            for M in max_ideals:
                S = set(range(n)) - M
                if not is_multiplicatively_closed(n, mul, S):
                    raise ValueError("Localization undefined")
                    
                if not check_IM_sub_JM(n, add, mul, neg, I, J, S):
                    rhs_true = False
                    break
                    
            equiv = (I_sub_J == rhs_true)
            neg_Q = not equiv
    except Exception:
        neg_Q = True
        
    return [h1_ok, h2_ok, neg_Q]