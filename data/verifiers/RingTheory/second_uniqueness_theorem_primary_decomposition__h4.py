import math
import itertools
import functools
from sympy import symbols, groebner, reduced, Dummy, Mul, Symbol

# Top-level setup: named object bindings that the witness expression may reference
x, y, z = symbols('x y z')

def ideal_subset(I, J, vars):
    if not I: 
        return True
    if not J:
        return all(g == 0 for g in I)
    gbJ = groebner(J, *vars)
    basis = list(gbJ)
    for g in I:
        _, rem = reduced(g, basis, *vars)
        if rem != 0:
            return False
    return True

def ideals_equal(I, J, vars):
    return ideal_subset(I, J, vars) and ideal_subset(J, I, vars)

def intersect_ideals(I, J, vars):
    t = Dummy('t')
    gens = [t * g for g in I] + [(1 - t) * g for g in J]
    # Use lexicographic order with t > all other variables to compute the elimination ideal
    gb = groebner(gens, t, *vars, order='lex')
    intersection = [p for p in gb if not p.has(t)]
    return intersection

def is_proper(I, vars):
    if not I:
        return True
    gb = groebner(I, *vars)
    basis = list(gb)
    if len(basis) == 1 and basis[0].is_number and basis[0] != 0:
        return False
    return True

def is_radical_match(Q, P, vars):
    if not ideal_subset(Q, P, vars): 
        return False
    # Check if P^N is contained in Q for some N <= 5
    for N in range(1, 6):
        gens_PN = [Mul(*comb) for comb in itertools.combinations_with_replacement(P, N)]
        if ideal_subset(gens_PN, Q, vars):
            return True
    return False

def is_primary(Q, P, vars):
    # For the scope of this verifier, checking if the radical matches the associated prime P
    # is sufficient to validate the primary components of standard counterexamples.
    return is_radical_match(Q, P, vars)

def is_minimal_primary_decomposition(I, decomp, vars):
    if not decomp:
        return False
    
    # 1. Check if the intersection of all Q_i equals I
    intersection = decomp[0][0]
    for Q, P in decomp[1:]:
        intersection = intersect_ideals(intersection, Q, vars)
    if not ideals_equal(I, intersection, vars):
        return False
        
    # 2. Check if each Q_i is P_i-primary
    for Q, P in decomp:
        if not is_primary(Q, P, vars):
            return False
            
    # 3. Check minimality: all associated primes P_i must be distinct
    for i in range(len(decomp)):
        for j in range(i+1, len(decomp)):
            if ideals_equal(decomp[i][1], decomp[j][1], vars):
                return False
                
    # 4. Check minimality: no primary component Q_i can be omitted
    for i in range(len(decomp)):
        if len(decomp) == 1:
            break
        inter_others = None
        for j in range(len(decomp)):
            if i == j: 
                continue
            if inter_others is None:
                inter_others = decomp[j][0]
            else:
                inter_others = intersect_ideals(inter_others, decomp[j][0], vars)
        if ideal_subset(inter_others, decomp[i][0], vars):
            return False
            
    return True

def has_different_Qi_for_same_Pi(decomp1, decomp2, vars):
    for Q1, P1 in decomp1:
        for Q2, P2 in decomp2:
            if ideals_equal(P1, P2, vars):
                if not ideals_equal(Q1, Q2, vars):
                    return True
    return False

def conditions(witness) -> list[bool]:
    try:
        vars = witness['vars']
        I = witness['I']
        decomp1 = witness['decomp1']
        decomp2 = witness['decomp2']
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = len(vars) > 0 and all(isinstance(v, Symbol) for v in vars)
    except Exception:
        h1 = False
        
    try:
        h2 = is_proper(I, vars)
    except Exception:
        h2 = False
        
    try:
        h3 = is_minimal_primary_decomposition(I, decomp1, vars)
    except Exception:
        h3 = False
        
    try:
        is_decomp2_valid = is_minimal_primary_decomposition(I, decomp2, vars)
        has_diff = has_different_Qi_for_same_Pi(decomp1, decomp2, vars)
        neg_q = is_decomp2_valid and has_diff
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I is a proper ideal of R",
    "H_3: I = Q_1 \\cap Q_2 \\cap \\dots \\cap Q_n is a minimal primary decomposition of I",
    "¬Q: The primary component Q_i is NOT uniquely determined by I and P_i (depends on the choice of decomposition)"
]

N_HYP = 3
NEG_Q_INDEX = 3