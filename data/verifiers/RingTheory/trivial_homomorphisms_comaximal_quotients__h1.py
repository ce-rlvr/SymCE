import z3
import math
import itertools
import functools
import sympy

# Top-level setup
x, y, z = sympy.symbols('x y z')

def is_ring(n, add, mult):
    if not isinstance(n, int) or n <= 0: return False
    if len(add) != n or len(mult) != n: return False
    for i in range(n):
        if len(add[i]) != n or len(mult[i]) != n: return False
        for j in range(n):
            if not isinstance(add[i][j], int) or not (0 <= add[i][j] < n): return False
            if not isinstance(mult[i][j], int) or not (0 <= mult[i][j] < n): return False
            
    # Additive identity (must be 0)
    for i in range(n):
        if add[i][0] != i or add[0][i] != i: return False
        
    # Additive inverse
    for i in range(n):
        has_inv = False
        for j in range(n):
            if add[i][j] == 0 and add[j][i] == 0:
                has_inv = True
                break
        if not has_inv: return False
        
    # Commutativity of addition
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            
    # Associativity of addition
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                
    # Associativity of multiplication
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mult[mult[i][j]][k] != mult[i][mult[j][k]]: return False
                
    # Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mult[i][add[j][k]] != add[mult[i][j]][mult[i][k]]: return False
                if mult[add[i][j]][k] != add[mult[i][k]][mult[j][k]]: return False
                
    return True

def is_ideal(n, add, mult, I):
    if not I: return False
    I_set = set(I)
    if len(I_set) != len(I): return False
    for val in I:
        if not isinstance(val, int) or not (0 <= val < n): return False
    if 0 not in I_set: return False
    
    # Closed under addition
    for val1 in I:
        for val2 in I:
            if add[val1][val2] not in I_set: return False
            
    # Absorbs multiplication from both sides
    for val in I:
        for r in range(n):
            if mult[r][val] not in I_set: return False
            if mult[val][r] not in I_set: return False
            
    return True

def is_comaximal(n, add, I, J):
    I_set = set(I)
    J_set = set(J)
    sums = set()
    for i in I_set:
        for j in J_set:
            sums.add(add[i][j])
    return len(sums) == n

def get_cosets(n, add, I):
    I_set = set(I)
    cosets = []
    seen = set()
    for i in range(n):
        if i not in seen:
            coset = set()
            for val in I_set:
                coset.add(add[i][val])
            cosets.append(frozenset(coset))
            seen.update(coset)
    if sum(len(c) for c in cosets) != n:
        raise ValueError("Not a valid partition")
    return cosets

def build_quotient_module(n, add, mult, I):
    cosets = get_cosets(n, add, I)
    coset_to_idx = {c: idx for idx, c in enumerate(cosets)}
    
    zero_idx = None
    for c, idx in coset_to_idx.items():
        if 0 in c:
            zero_idx = idx
            break
            
    add_q = {}
    for c1, i1 in coset_to_idx.items():
        for c2, i2 in coset_to_idx.items():
            rep1 = next(iter(c1))
            rep2 = next(iter(c2))
            sum_rep = add[rep1][rep2]
            for c3, i3 in coset_to_idx.items():
                if sum_rep in c3:
                    add_q[(i1, i2)] = i3
                    break
                    
    mult_q = {}
    for r in range(n):
        for c, i in coset_to_idx.items():
            rep = next(iter(c))
            prod_rep = mult[r][rep]
            for c3, i3 in coset_to_idx.items():
                if prod_rep in c3:
                    mult_q[(r, i)] = i3
                    break
                    
    return len(cosets), zero_idx, add_q, mult_q

def has_nonzero_homomorphism_z3(n, add, mult, I, J):
    n_I, zero_I, add_I, mult_I = build_quotient_module(n, add, mult, I)
    n_J, zero_J, add_J, mult_J = build_quotient_module(n, add, mult, J)
    
    solver = z3.Solver()
    f = [z3.Int(f"f_{i}") for i in range(n_I)]
    
    for i in range(n_I):
        solver.add(f[i] >= 0, f[i] < n_J)
        
    solver.add(f[zero_I] == zero_J)
    
    uid = id(solver)
    Add_J = z3.Function(f'Add_J_{uid}', z3.IntSort(), z3.IntSort(), z3.IntSort())
    for x_val in range(n_J):
        for y_val in range(n_J):
            solver.add(Add_J(x_val, y_val) == add_J[(x_val, y_val)])
            
    for i in range(n_I):
        for j in range(n_I):
            solver.add(f[add_I[(i, j)]] == Add_J(f[i], f[j]))
            
    Mult_J = z3.Function(f'Mult_J_{uid}', z3.IntSort(), z3.IntSort(), z3.IntSort())
    for r in range(n):
        for x_val in range(n_J):
            solver.add(Mult_J(r, x_val) == mult_J[(r, x_val)])
            
    for r in range(n):
        for i in range(n_I):
            solver.add(f[mult_I[(r, i)]] == Mult_J(r, f[i]))
            
    solver.add(z3.Or([f[i] != zero_J for i in range(n_I)]))
    
    return solver.check() == z3.sat

def conditions(witness):
    """
    witness format: (n, add, mult, I, J)
    where:
      n: int, size of the ring
      add: list of lists of ints, addition table
      mult: list of lists of ints, multiplication table
      I: list of ints, elements of ideal I
      J: list of ints, elements of ideal J
    """
    try:
        n, add, mult, I, J = witness
        h1 = is_ring(n, add, mult) and is_ideal(n, add, mult, I) and is_ideal(n, add, mult, J) and is_comaximal(n, add, I, J)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = has_nonzero_homomorphism_z3(n, add, mult, I, J)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are comaximal ideals of R",
    "¬Q: There exists a non-zero R-module homomorphism from R/I to R/J"
]

N_HYP = 1
NEG_Q_INDEX = 1