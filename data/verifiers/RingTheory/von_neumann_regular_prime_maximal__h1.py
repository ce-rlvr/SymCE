import sympy
from sympy.matrices import eye, zeros
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: For every element a in R, there exists an element x in R such that a = (a^2) * x",
    "H_2: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_witness_attrs(witness):
    try:
        R = witness.R
        P = witness.P
        add = witness.add
        mul = witness.mul
        return R, P, add, mul
    except AttributeError:
        pass
    try:
        return witness['R'], witness['P'], witness['add'], witness['mul']
    except (TypeError, KeyError):
        pass
    return witness[0], witness[1], witness[2], witness[3]

def to_set(iterable):
    try:
        return set(iterable)
    except TypeError:
        res = []
        for x in iterable:
            if x not in res:
                res.append(x)
        return res

def add_to_set(collection, item):
    if isinstance(collection, set):
        if item not in collection:
            collection.add(item)
            return True
        return False
    else:
        if item not in collection:
            collection.append(item)
            return True
        return False

def generate_ideal(R_set, generators, add, mul):
    ideal = list(generators)
    ideal_set = to_set(ideal)
    max_size = len(R_set)
    
    head = 0
    while head < len(ideal):
        if len(ideal_set) > max_size:
            break
        x = ideal[head]
        head += 1
        
        for y in ideal:
            s1 = add(x, y)
            if add_to_set(ideal_set, s1):
                ideal.append(s1)
            s2 = add(y, x)
            if add_to_set(ideal_set, s2):
                ideal.append(s2)
                
        for r in R_set:
            m1 = mul(r, x)
            if add_to_set(ideal_set, m1):
                ideal.append(m1)
            m2 = mul(x, r)
            if add_to_set(ideal_set, m2):
                ideal.append(m2)
                
    return ideal_set

def conditions(witness):
    try:
        R, P, add, mul = get_witness_attrs(witness)
        R_set = to_set(R)
    except Exception:
        return [False, False, False]
        
    # H1: For every element a in R, there exists an element x in R such that a = (a^2) * x
    try:
        h1_ok = True
        for a in R_set:
            a2 = mul(a, a)
            found = False
            for x in R_set:
                if mul(a2, x) == a:
                    found = True
                    break
            if not found:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H2: P is a prime ideal of R
    try:
        h2_ok = True
        P_set = to_set(P)
        
        if not P_set or not all(p in R_set for p in P_set) or len(P_set) == len(R_set):
            h2_ok = False
        else:
            is_ideal = True
            for x in P_set:
                for y in P_set:
                    if add(x, y) not in P_set:
                        is_ideal = False
                        break
                for r in R_set:
                    if mul(r, x) not in P_set or mul(x, r) not in P_set:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
            
            if not is_ideal:
                h2_ok = False
            else:
                is_prime = True
                for a in R_set:
                    if a in P_set: continue
                    for b in R_set:
                        if b in P_set: continue
                        
                        ideal_a = generate_ideal(R_set, [a], add, mul)
                        ideal_b = generate_ideal(R_set, [b], add, mul)
                        
                        subset = True
                        for x in ideal_a:
                            for y in ideal_b:
                                if mul(x, y) not in P_set:
                                    subset = False
                                    break
                            if not subset:
                                break
                        
                        if subset:
                            is_prime = False
                            break
                    if not is_prime:
                        break
                h2_ok = is_prime
    except Exception:
        h2_ok = False

    # neg_Q: P is not a maximal ideal of R
    try:
        is_maximal = True
        P_set = to_set(P)
        if not all(p in R_set for p in P_set) or len(P_set) == len(R_set):
            is_maximal = False
        else:
            for x in R_set:
                if x not in P_set:
                    gen = list(P_set)
                    gen.append(x)
                    ideal_x = generate_ideal(R_set, gen, add, mul)
                    if len(ideal_x) < len(R_set):
                        is_maximal = False
                        break
        neg_q_ok = not is_maximal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]