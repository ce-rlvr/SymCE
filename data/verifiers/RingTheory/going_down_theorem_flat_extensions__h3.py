import sympy as sp
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t, u, v = sp.symbols('x y z t u v')

def ideal_subset(I_gens, J_gens, vars):
    J_gens = [g for g in J_gens if g != 0]
    if not J_gens:
        return all(sp.expand(f) == 0 for f in I_gens)
    gb = sp.groebner(J_gens, *vars, domain='QQ')
    for f in I_gens:
        if f != 0 and gb.reduce(f)[1] != 0:
            return False
    return True

def ideals_equal(I_gens, J_gens, vars):
    return ideal_subset(I_gens, J_gens, vars) and ideal_subset(J_gens, I_gens, vars)

def ideal_intersection_subring(I_gens, vars_all, vars_sub):
    I_gens = [f for f in I_gens if f != 0]
    if not I_gens:
        return []
    vars_elim = [var for var in vars_all if var not in vars_sub]
    if not vars_elim:
        return I_gens
    
    gb = sp.groebner(I_gens, *(vars_elim + vars_sub), order='lex', domain='QQ')
    
    intersect_gens = []
    for f in gb:
        if not any(var in f.free_symbols for var in vars_elim):
            intersect_gens.append(f)
    return intersect_gens

def check_subring(vars_R, vars_S, I_R, I_S):
    if not all(var in vars_S for var in vars_R):
        return False
    intersect_gens = ideal_intersection_subring(I_S, vars_S, vars_R)
    return ideals_equal(intersect_gens, I_R, vars_R)

def is_prime_ideal(I_gens, vars):
    I_gens = [f for f in I_gens if f != 0]
    if not I_gens:
        return True
    
    gb = sp.groebner(I_gens, *vars, domain='QQ')
    gb_gens = list(gb)
    
    if len(gb_gens) == 1:
        f = gb_gens[0]
        factors = sp.factor_list(f, domain='QQ')[1]
        if len(factors) == 1 and factors[0][1] == 1:
            return True
        return False
    
    if len(gb_gens) == len(vars):
        is_linear = True
        for f in gb_gens:
            poly = f.as_poly(*vars)
            if poly is None or poly.total_degree() != 1:
                is_linear = False
                break
        if is_linear:
            sols = sp.solve(gb_gens, vars, dict=True)
            if isinstance(sols, list) and len(sols) == 1:
                sol = sols[0]
                if all(sp.sympify(sol.get(var, 0)).is_Rational for var in vars):
                    return True
                    
    return False

def check_negated_conclusion(witness):
    vars_R = witness['vars_R']
    vars_S = witness['vars_S']
    I_R = witness.get('I_R', [])
    I_S = witness.get('I_S', [])
    P1 = witness['P1']
    Q2 = witness['Q2']
    S_min_primes = witness['S_min_primes']
    
    # Verify that the provided minimal primes are indeed prime ideals containing I_S
    for M in S_min_primes:
        M_QQ = M + I_S
        if not is_prime_ideal(M_QQ, vars_S):
            return False
        if not ideal_subset(I_S, M_QQ, vars_S):
            return False
            
    # Verify that the product of the provided minimal primes is contained in I_S
    # This proves that any prime ideal Q1 containing I_S must contain at least one of these M
    prod_gens = [sp.sympify(1)]
    for M in S_min_primes:
        M_QQ = M + I_S
        if not M_QQ:
            M_QQ = [sp.sympify(0)]
        new_prod_gens = []
        for p1 in prod_gens:
            for p2 in M_QQ:
                new_prod_gens.append(p1 * p2)
        prod_gens = new_prod_gens
        
    if not ideal_subset(prod_gens, I_S, vars_S):
        return False
        
    P1_QQ = P1 + I_R
    Q2_QQ = Q2 + I_S
    
    # If for every minimal prime M, any Q1 containing M fails the conditions,
    # then no valid Q1 can exist.
    for M in S_min_primes:
        M_QQ = M + I_S
        m_subset_q2 = ideal_subset(M_QQ, Q2_QQ, vars_S)
        
        m_cap_R = ideal_intersection_subring(M_QQ, vars_S, vars_R)
        m_cap_R_subset_p1 = ideal_subset(m_cap_R, P1_QQ, vars_R)
        
        # If M is subset of Q2 AND M \cap R is subset of P1, then M itself (or a larger prime)
        # might be a valid Q1. The witness fails to prove non-existence.
        if m_subset_q2 and m_cap_R_subset_p1:
            return False
            
    return True

def conditions(witness):
    try:
        vars_R = witness['vars_R']
        vars_S = witness['vars_S']
        I_R = witness.get('I_R', [])
        I_S = witness.get('I_S', [])
        P1 = witness['P1']
        P2 = witness['P2']
        Q2 = witness['Q2']
        S_min_primes = witness['S_min_primes']
    except (KeyError, TypeError):
        return [False] * 5

    # H1: R and S are commutative rings
    try:
        h1 = isinstance(vars_R, list) and isinstance(vars_S, list)
    except Exception:
        h1 = False

    # H2: R is a subring of S
    try:
        h2 = check_subring(vars_R, vars_S, I_R, I_S)
    except Exception:
        h2 = False

    # H3: P_1 and P_2 are prime ideals of R such that P_1 \subseteq P_2
    try:
        P1_QQ = P1 + I_R
        P2_QQ = P2 + I_R
        h3 = is_prime_ideal(P1_QQ, vars_R) and is_prime_ideal(P2_QQ, vars_R) and ideal_subset(P1_QQ, P2_QQ, vars_R)
    except Exception:
        h3 = False

    # H4: Q_2 is a prime ideal of S such that Q_2 \cap R = P_2
    try:
        Q2_QQ = Q2 + I_S
        intersect_gens = ideal_intersection_subring(Q2_QQ, vars_S, vars_R)
        h4 = is_prime_ideal(Q2_QQ, vars_S) and ideals_equal(intersect_gens, P2_QQ, vars_R)
    except Exception:
        h4 = False

    # Negated Conclusion
    try:
        neg_q = check_negated_conclusion(witness)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: R is a subring of S",
    "H_3: P_1 and P_2 are prime ideals of R such that P_1 \\subseteq P_2",
    "H_4: Q_2 is a prime ideal of S such that Q_2 \\cap R = P_2",
    "¬Q: No prime ideal Q_1 of S satisfies Q_1 \\subseteq Q_2 and Q_1 \\cap R = P_1"
]

N_HYP = 4
NEG_Q_INDEX = 4