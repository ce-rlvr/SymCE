import sympy
from sympy import symbols, Rational, Integer
import itertools
import functools
import math

# Top-level setup
x, y, z = symbols('x y z')

def get_all_ideals(elements, add, mul, zero):
    principal_ideals = []
    for el in elements:
        closure = set([el])
        while True:
            new_elements = set(closure)
            for a in closure:
                for b in closure:
                    new_elements.add(add(a, b))
            for a in closure:
                for r in elements:
                    new_elements.add(mul(r, a))
                    new_elements.add(mul(a, r))
            if len(new_elements) == len(closure):
                break
            closure = new_elements
        principal_ideals.append(frozenset(closure))
    
    principal_ideals = set(principal_ideals)
    all_ideals = set(principal_ideals)
    while True:
        new_ideals = set(all_ideals)
        for I1 in all_ideals:
            for I2 in principal_ideals:
                sum_ideal = set()
                for a in I1:
                    for b in I2:
                        sum_ideal.add(add(a, b))
                new_ideals.add(frozenset(sum_ideal))
        if len(new_ideals) == len(all_ideals):
            break
        all_ideals = new_ideals
    return all_ideals

def get_all_prime_ideals(all_ideals, elements, add, mul, zero):
    prime_ideals = set()
    for P in all_ideals:
        P_set = set(P)
        if len(P_set) == len(elements):
            continue
        not_in_P = [el for el in elements if el not in P_set]
        is_prime = True
        for a in not_in_P:
            for b in not_in_P:
                all_in_P = True
                for r in elements:
                    if mul(a, mul(r, b)) not in P_set:
                        all_in_P = False
                        break
                if all_in_P:
                    is_prime = False
                    break
            if not is_prime:
                break
        if is_prime:
            prime_ideals.add(P)
    return prime_ideals

def radical_ideal_theoretic(Q, prime_ideals, elements):
    Q_set = set(Q)
    containing_primes = [P for P in prime_ideals if Q_set.issubset(P)]
    if not containing_primes:
        return frozenset(elements)
    res = set(containing_primes[0])
    for P in containing_primes[1:]:
        res = res.intersection(P)
    return frozenset(res)

def is_primary_ideal_theoretic(Q, rad_Q, elements, add, mul, zero):
    Q_set = set(Q)
    rad_set = set(rad_Q)
    not_in_Q = [el for el in elements if el not in Q_set]
    not_in_rad = [el for el in elements if el not in rad_set]
    for a in not_in_Q:
        for b in not_in_rad:
            all_in_Q = True
            for r in elements:
                if mul(a, mul(r, b)) not in Q_set:
                    all_in_Q = False
                    break
            if all_in_Q:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            I = witness['I']
            Q_list = witness['Q']
            Q_prime_list = witness['Q_prime']
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            I = witness.I
            Q_list = witness.Q
            Q_prime_list = witness.Q_prime
    except Exception:
        return [False, False, False, False]

    try:
        all_ideals = get_all_ideals(elements, add, mul, zero)
        prime_ideals = get_all_prime_ideals(all_ideals, elements, add, mul, zero)
    except Exception:
        return [False, False, False, False]

    def check_proper(ideal_I):
        if frozenset(ideal_I) not in all_ideals:
            return False
        return set(ideal_I) != set(elements)

    def check_minimal_primary_decomp(q_list):
        if not q_list:
            return False
        
        intersect = set(q_list[0])
        for q in q_list[1:]:
            intersect = intersect.intersection(set(q))
        if intersect != set(I):
            return False
            
        for q in q_list:
            if frozenset(q) not in all_ideals:
                return False
            rad_q = radical_ideal_theoretic(q, prime_ideals, elements)
            if not is_primary_ideal_theoretic(q, rad_q, elements, add, mul, zero):
                return False
                
        for i in range(len(q_list)):
            other_ideals = q_list[:i] + q_list[i+1:]
            if not other_ideals:
                continue
            intersect_other = set(other_ideals[0])
            for q in other_ideals[1:]:
                intersect_other = intersect_other.intersection(set(q))
            if intersect_other == set(I):
                return False
                
        rads = [radical_ideal_theoretic(q, prime_ideals, elements) for q in q_list]
        if len(set(rads)) != len(rads):
            return False
            
        return True

    try:
        h1 = check_proper(I)
    except Exception:
        h1 = False

    try:
        h2 = check_minimal_primary_decomp(Q_list)
    except Exception:
        h2 = False

    try:
        h3 = check_minimal_primary_decomp(Q_prime_list)
    except Exception:
        h3 = False

    try:
        n = len(Q_list)
        m = len(Q_prime_list)
        
        rads_Q = set([radical_ideal_theoretic(q, prime_ideals, elements) for q in Q_list])
        rads_Q_prime = set([radical_ideal_theoretic(q, prime_ideals, elements) for q in Q_prime_list])
        
        all_prime = True
        for r in rads_Q.union(rads_Q_prime):
            if r not in prime_ideals:
                all_prime = False
                break
                
        if n == m and rads_Q == rads_Q_prime and all_prime:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: Q_list is a minimal primary decomposition of I",
    "H_3: Q_prime_list is a minimal primary decomposition of I",
    "¬Q: n != m or the sets of prime ideals are not identical"
]

N_HYP = 3
NEG_Q_INDEX = 3