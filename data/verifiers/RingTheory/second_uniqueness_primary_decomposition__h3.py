import sympy
from sympy import Dummy, groebner

# Top-level setup
x, y, z, t = sympy.symbols('x y z t')

def ideal_contains(I_gens, J_gens, vars):
    if not I_gens: I_gens = [0]
    if not J_gens: J_gens = [0]
    try:
        G = groebner(I_gens, *vars)
        for g in J_gens:
            if G.reduce(g)[1] != 0:
                return False
        return True
    except Exception:
        return False

def ideal_eq(I_gens, J_gens, vars):
    return ideal_contains(I_gens, J_gens, vars) and ideal_contains(J_gens, I_gens, vars)

def intersect_ideals(I_gens, J_gens, vars):
    if not I_gens: I_gens = [0]
    if not J_gens: J_gens = [0]
    t_dummy = Dummy('t')
    gens = [t_dummy * g for g in I_gens] + [(1 - t_dummy) * g for g in J_gens]
    try:
        G = groebner(gens, *([t_dummy] + vars), order='lex')
        return [g for g in G if not g.has(t_dummy)]
    except Exception:
        return [0]

def is_radical_of(P_gens, Q_gens, vars):
    if not ideal_contains(P_gens, Q_gens, vars):
        return False
    for g in P_gens:
        found = False
        for m in range(1, 10):
            if ideal_contains(Q_gens, [g**m], vars):
                found = True
                break
        if not found:
            return False
    return True

def check_decomp(I, decomp, vars):
    if not decomp: return False
    intersect = decomp[0]
    for Q in decomp[1:]:
        intersect = intersect_ideals(intersect, Q, vars)
    return ideal_eq(I, intersect, vars)

def is_minimal_decomp(I, decomp, vars):
    if not check_decomp(I, decomp, vars):
        return False
    for i in range(len(decomp)):
        if len(decomp) == 1:
            break
        intersect = decomp[0] if i != 0 else decomp[1]
        for j in range(len(decomp)):
            if j != i and j != (0 if i != 0 else 1):
                intersect = intersect_ideals(intersect, decomp[j], vars)
        if ideal_contains(decomp[i], intersect, vars):
            return False
    return True

def check_radicals(decomp, primes, vars):
    if len(decomp) != len(primes): return False
    for Q, P in zip(decomp, primes):
        if not is_radical_of(P, Q, vars):
            return False
    return True

def is_minimal_prime(P, primes, vars):
    found = False
    for p in primes:
        if ideal_eq(P, p, vars):
            found = True
            break
    if not found: return False
    
    for p in primes:
        if not ideal_eq(P, p, vars):
            if ideal_contains(P, p, vars):
                return False
    return True

def conditions(witness):
    try:
        vars = witness['vars']
        I = witness['I']
        P = witness['P']
        decomp1 = witness['decomp1']
        primes1 = witness['primes1']
        decomp2 = witness['decomp2']
        primes2 = witness['primes2']
        
        # H1: R is a commutative ring
        h1 = True
        
        # H2: I is a proper ideal of R
        h2 = not ideal_contains(I, [1], vars)
        
        # H3: P_i = \sqrt{Q_i} is a minimal element in the set of associated primes
        h3 = False
        if is_minimal_decomp(I, decomp1, vars) and check_radicals(decomp1, primes1, vars):
            if is_minimal_prime(P, primes1, vars):
                h3 = True
                
        # neg_Q: The primary component Q_i is NOT uniquely determined by I
        neg_q = False
        if h3:
            if is_minimal_decomp(I, decomp2, vars) and check_radicals(decomp2, primes2, vars):
                q1_found = None
                for Q, p in zip(decomp1, primes1):
                    if ideal_eq(p, P, vars):
                        q1_found = Q
                        break
                q2_found = None
                for Q, p in zip(decomp2, primes2):
                    if ideal_eq(p, P, vars):
                        q2_found = Q
                        break
                if q1_found is not None and q2_found is not None:
                    if not ideal_eq(q1_found, q2_found, vars):
                        neg_q = True
                        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a proper ideal of R",
    "H_3: P_i = \\sqrt{Q_i} is a minimal element in the set of associated primes of I with respect to inclusion",
    "¬Q: The primary component Q_i is NOT uniquely determined by I (it depends on the choice of the minimal primary decomposition)"
]

N_HYP = 3
NEG_Q_INDEX = 3