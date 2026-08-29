import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
import math
import z3

# Top-level setup: named object bindings
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

def check_finite_ring(n, add_table, mul_table, x_idx):
    if n == 0: 
        return False, False
    
    # Check addition abelian group axioms
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if add_table[add_table[a][b]][c] != add_table[a][add_table[b][c]]:
                    return False, False
    for a in range(n):
        for b in range(n):
            if add_table[a][b] != add_table[b][a]:
                return False, False
                
    zero = None
    for a in range(n):
        if all(add_table[a][b] == b for b in range(n)):
            zero = a
            break
    if zero is None: 
        return False, False
    
    # Check multiplication associativity and distributivity
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if mul_table[mul_table[a][b]][c] != mul_table[a][mul_table[b][c]]:
                    return False, False
                    
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if mul_table[a][add_table[b][c]] != add_table[mul_table[a][b]][mul_table[a][c]]:
                    return False, False
                if mul_table[add_table[a][b]][c] != add_table[mul_table[a][c]][mul_table[b][c]]:
                    return False, False
                    
    if not (0 <= x_idx < n):
        return False, False
            
    def generate_ideal(generators):
        ideal = set(generators)
        ideal.add(zero)
        while True:
            size_before = len(ideal)
            new_elements = set()
            for a in list(ideal):
                for b in list(ideal):
                    new_elements.add(add_table[a][b])
                for r in range(n):
                    new_elements.add(mul_table[r][a])
                    new_elements.add(mul_table[a][r])
            ideal.update(new_elements)
            if len(ideal) == size_before:
                break
        return frozenset(ideal)

    principal_ideals = set()
    for i in range(n):
        principal_ideals.add(generate_ideal([i]))
        
    ideals = set(principal_ideals)
    while True:
        size_before = len(ideals)
        new_ideals = set()
        for I in list(ideals):
            for J in principal_ideals:
                combined = generate_ideal(set(I) | set(J))
                new_ideals.add(combined)
        ideals.update(new_ideals)
        if len(ideals) == size_before:
            break
                
    proper_ideals = [I for I in ideals if len(I) < n]
    
    maximal_ideals = []
    for I in proper_ideals:
        is_maximal = True
        for J in proper_ideals:
            if I != J and I.issubset(J):
                is_maximal = False
                break
        if is_maximal:
            maximal_ideals.append(I)
            
    cond2 = True
    for M in maximal_ideals:
        found_s = False
        for s in range(n):
            if s not in M:
                if mul_table[s][x_idx] == zero and mul_table[x_idx][s] == zero:
                    found_s = True
                    break
        if not found_s:
            cond2 = False
            break
            
    return True, cond2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # 1. Witness is a SymPy Matrix (representing an element of M_n(Q))
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            if witness.shape[0] == witness.shape[1]:
                h1 = True
                det_val = sympy.simplify(witness.det())
                h2 = bool(det_val == 0)
                neg_q = not witness.is_zero_matrix
                return [h1, h2, neg_q]
                
        # 2. Witness is a tuple (n, mul_table, x) representing a ring on Z_n
        if isinstance(witness, tuple) and len(witness) == 3:
            n, mul_table, x = witness
            if isinstance(n, int) and n > 0:
                add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
                is_ring, cond2 = check_finite_ring(n, add_table, mul_table, x)
                if is_ring:
                    h1 = True
                    h2 = cond2
                    neg_q = (x != 0)
                    return [h1, h2, neg_q]
                    
        # 3. Witness is a tuple (elements, add_table, mul_table, x)
        if isinstance(witness, tuple) and len(witness) == 4:
            elements, add_table, mul_table, x = witness
            if isinstance(elements, list):
                elem_to_idx = {e: i for i, e in enumerate(elements)}
                n = len(elements)
                add_idx = [[elem_to_idx[add_table[i][j]] for j in range(n)] for i in range(n)]
                mul_idx = [[elem_to_idx[mul_table[i][j]] for j in range(n)] for i in range(n)]
                x_idx = elem_to_idx[x]
                is_ring, cond2 = check_finite_ring(n, add_idx, mul_idx, x_idx)
                if is_ring:
                    h1 = True
                    h2 = cond2
                    zero_idx = None
                    for a in range(n):
                        if all(add_idx[a][b] == b for b in range(n)):
                            zero_idx = a
                            break
                    neg_q = (x_idx != zero_idx)
                    return [h1, h2, neg_q]
                    
        # 4. Witness is an object with elements, add, mul, x
        if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'x'):
            elements = witness.elements
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            n = len(elements)
            add_idx = [[0]*n for _ in range(n)]
            mul_idx = [[0]*n for _ in range(n)]
            for i, a in enumerate(elements):
                for j, b in enumerate(elements):
                    add_idx[i][j] = elem_to_idx[witness.add(a, b)]
                    mul_idx[i][j] = elem_to_idx[witness.mul(a, b)]
            x_idx = elem_to_idx[witness.x]
            is_ring, cond2 = check_finite_ring(n, add_idx, mul_idx, x_idx)
            if is_ring:
                h1 = True
                h2 = cond2
                zero_idx = None
                for a in range(n):
                    if all(add_idx[a][b] == b for b in range(n)):
                        zero_idx = a
                        break
                neg_q = (x_idx != zero_idx)
                return [h1, h2, neg_q]
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "H_2: For every maximal ideal M of R, the image of x in the localization R_M is zero",
    "¬Q: x != 0 in R"
]

N_HYP = 2
NEG_Q_INDEX = 2