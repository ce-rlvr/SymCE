import sympy
from sympy import Rational, Integer
import itertools
import functools

# Top-level setup
# (No specific named bindings required for this custom ring representation,
# but we provide standard SymPy tools if needed)

def get_table(elems, op):
    if isinstance(op, dict):
        return op
    elif isinstance(op, (list, tuple)):
        return {(a, b): op[a][b] for a in elems for b in elems}
    else:
        return {(a, b): op(a, b) for a in elems for b in elems}

def get_func(elems, f):
    if isinstance(f, dict):
        return f
    elif isinstance(f, (list, tuple)):
        return {a: f[a] for a in elems}
    else:
        return {a: f(a) for a in elems}

def parse_witness(witness):
    if len(witness) == 4:
        n, m, f, X = witness
        elems_R = list(range(n))
        add_R = {(a, b): (a + b) % n for a in elems_R for b in elems_R}
        mul_R = {(a, b): (a * b) % n for a in elems_R for b in elems_R}
        elems_S = list(range(m))
        add_S = {(a, b): (a + b) % m for a in elems_S for b in elems_S}
        mul_S = {(a, b): (a * b) % m for a in elems_S for b in elems_S}
        f_dict = get_func(elems_R, f)
        return elems_R, add_R, mul_R, elems_S, add_S, mul_S, f_dict, X
    elif len(witness) == 8:
        elems_R, add_R, mul_R, elems_S, add_S, mul_S, f, X = witness
        add_R_dict = get_table(elems_R, add_R)
        mul_R_dict = get_table(elems_R, mul_R)
        add_S_dict = get_table(elems_S, add_S)
        mul_S_dict = get_table(elems_S, mul_S)
        f_dict = get_func(elems_R, f)
        return elems_R, add_R_dict, mul_R_dict, elems_S, add_S_dict, mul_S_dict, f_dict, X
    else:
        raise ValueError("Invalid witness format. Expected 4 or 8 elements.")

def is_ring(elems, add, mul):
    if not elems: return False
    # closure
    for a in elems:
        for b in elems:
            if (a, b) not in add or add[(a, b)] not in elems: return False
            if (a, b) not in mul or mul[(a, b)] not in elems: return False
    # addition associativity
    for a in elems:
        for b in elems:
            for c in elems:
                if add[(add[(a, b)], c)] != add[(a, add[(b, c)])]: return False
    # addition commutativity
    for a in elems:
        for b in elems:
            if add[(a, b)] != add[(b, a)]: return False
    # zero
    zeros = [z for z in elems if all(add[(z, a)] == a for a in elems)]
    if not zeros: return False
    zero = zeros[0]
    # inverses
    for a in elems:
        if not any(add[(a, b)] == zero for b in elems): return False
    # multiplication associativity
    for a in elems:
        for b in elems:
            for c in elems:
                if mul[(mul[(a, b)], c)] != mul[(a, mul[(b, c)])]: return False
    # distributivity
    for a in elems:
        for b in elems:
            for c in elems:
                if mul[(a, add[(b, c)])] != add[(mul[(a, b)], mul[(a, c)])]: return False
                if mul[(add[(a, b)], c)] != add[(mul[(a, c)], mul[(b, c)])]: return False
    return True

def is_homomorphism(elems_R, add_R, mul_R, elems_S, add_S, mul_S, f):
    for a in elems_R:
        if a not in f or f[a] not in elems_S: return False
    for a in elems_R:
        for b in elems_R:
            if f[add_R[(a, b)]] != add_S[(f[a], f[b])]: return False
            if f[mul_R[(a, b)]] != mul_S[(f[a], f[b])]: return False
    ones_R = [u for u in elems_R if all(mul_R[(u, a)] == a and mul_R[(a, u)] == a for a in elems_R)]
    ones_S = [u for u in elems_S if all(mul_S[(u, a)] == a and mul_S[(a, u)] == a for a in elems_S)]
    if ones_R and ones_S:
        if f[ones_R[0]] != ones_S[0]: return False
    return True

def is_surjective(elems_R, elems_S, f):
    image = set(f[a] for a in elems_R if a in f)
    return set(elems_S) == image

def generated_subring(elems, add, mul, Y, include_one=True):
    zeros = [z for z in elems if all(add[(z, a)] == a for a in elems)]
    if not zeros: return set()
    zero = zeros[0]
    
    neg = {}
    for a in elems:
        for b in elems:
            if add[(a, b)] == zero:
                neg[a] = b
                break
                
    ones = [u for u in elems if all(mul[(u, a)] == a and mul[(a, u)] == a for a in elems)]
    
    gen = set(Y)
    if include_one and ones:
        gen.add(ones[0])
    if not gen:
        gen.add(zero)
        
    while True:
        new_gen = set(gen)
        for a in gen:
            for b in gen:
                if (a, b) in add:
                    new_gen.add(add[(a, b)])
                if (a, b) in mul:
                    new_gen.add(mul[(a, b)])
            if a in neg:
                new_gen.add(neg[a])
            
        if len(new_gen) == len(gen):
            break
        gen = new_gen
        
    return gen

def conditions(witness):
    try:
        elems_R, add_R, mul_R, elems_S, add_S, mul_S, f, X = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H1: R and S are rings
    try:
        h1 = is_ring(elems_R, add_R, mul_R) and is_ring(elems_S, add_S, mul_S)
    except Exception:
        h1 = False
        
    # H2: f is a surjective ring homomorphism
    try:
        h2_hom = is_homomorphism(elems_R, add_R, mul_R, elems_S, add_S, mul_S, f)
        h2_surj = is_surjective(elems_R, elems_S, f)
        h2 = h1 and h2_hom and h2_surj
    except Exception:
        h2 = False
        
    # neg_Q: f(X) does not generate S as a ring
    try:
        f_X = [f[x] for x in X if x in f]
        gen_S = generated_subring(elems_S, add_S, mul_S, f_X, include_one=True)
        neg_q = set(gen_S) != set(elems_S)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "¬Q: The image f(X) does not generate S as a ring"
]

N_HYP = 2
NEG_Q_INDEX = 2