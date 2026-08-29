import itertools
import sympy
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects are required for this domain, but we provide basic symbols.

def is_ring(R, add, mul):
    R_set = set(R)
    # check closure
    for a in R:
        for b in R:
            if add(a, b) not in R_set: return False
            if mul(a, b) not in R_set: return False
            
    # check add commutativity
    for a in R:
        for b in R:
            if add(a, b) != add(b, a): return False
            
    # check add associativity
    for a in R:
        for b in R:
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    # check mul associativity
    for a in R:
        for b in R:
            for c in R:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                
    # check distributivity
    for a in R:
        for b in R:
            for c in R:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    # check zero
    zeros = [e for e in R if all(add(e, _x) == _x for _x in R)]
    if not zeros: return False
    zero = zeros[0]
    
    # check add inverses
    for a in R:
        if not any(add(a, b) == zero for b in R): return False
        
    return True

def is_ideal(R, add, mul, S):
    if not S: return False
    S_set = set(S)
    if not S_set.issubset(set(R)): return False
    
    # check closed under addition
    for a in S:
        for b in S:
            if add(a, b) not in S_set:
                return False
                
    # check closed under outside multiplication
    for s in S:
        for r in R:
            if mul(r, s) not in S_set:
                return False
            if mul(s, r) not in S_set:
                return False
                
    # check if it's a subgroup under addition
    zeros = [e for e in R if all(add(e, _x) == _x for _x in R)]
    if not zeros: return False
    zero = zeros[0]
    if zero not in S_set: return False
    
    for s in S:
        if not any(add(s, _x) == zero for _x in S):
            return False
            
    return True

def get_all_ideals(R, add, mul):
    ideals = []
    R_list = list(R)
    for r in range(1, len(R_list) + 1):
        for subset in itertools.combinations(R_list, r):
            if is_ideal(R, add, mul, subset):
                ideals.append(subset)
    return ideals

def is_prime_ideal(R, add, mul, P, ideals):
    if not is_ideal(R, add, mul, P):
        return False
    if set(P) == set(R):
        return False
        
    P_set = set(P)
    for A in ideals:
        for B in ideals:
            ab_in_P = True
            for a in A:
                for b in B:
                    if mul(a, b) not in P_set:
                        ab_in_P = False
                        break
                if not ab_in_P:
                    break
            if ab_in_P:
                if not set(A).issubset(P_set) and not set(B).issubset(P_set):
                    return False
    return True

def get_all_prime_ideals(R, add, mul):
    ideals = get_all_ideals(R, add, mul)
    primes = []
    for P in ideals:
        if is_prime_ideal(R, add, mul, P, ideals):
            primes.append(P)
    return primes

def V(R, add, mul, I, primes):
    I_set = set(I)
    return [P for P in primes if I_set.issubset(set(P))]

def is_comaximal(R, add, I, J):
    I_plus_J = set()
    for i in I:
        for j in J:
            I_plus_J.add(add(i, j))
    return I_plus_J == set(R)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            I = witness['I']
            J = witness['J']
        else:
            R = witness.R
            add = witness.add
            mul = witness.mul
            I = witness.I
            J = witness.J
            
        # H1: I and J are ideals of R
        h1 = is_ring(R, add, mul) and is_ideal(R, add, mul, I) and is_ideal(R, add, mul, J)
        
        # H2: V(I) and V(J) denote the sets of prime ideals containing I and J
        primes = get_all_prime_ideals(R, add, mul)
        VI = V(R, add, mul, I, primes)
        VJ = V(R, add, mul, J, primes)
        h2 = isinstance(VI, list) and isinstance(VJ, list)
        
        # neg_Q: The conclusion is FALSE
        comaximal = is_comaximal(R, add, I, J)
        
        VI_set = set(frozenset(p) for p in VI)
        VJ_set = set(frozenset(p) for p in VJ)
        intersection_empty = len(VI_set.intersection(VJ_set)) == 0
        
        neg_q = (comaximal != intersection_empty)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: V(I) and V(J) denote the sets of prime ideals containing I and J",
    "¬Q: I and J are comaximal if and only if V(I) \\cap V(J) is empty is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2