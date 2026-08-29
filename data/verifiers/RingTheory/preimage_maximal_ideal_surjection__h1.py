import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def get_attr(w, name):
    if isinstance(w, dict):
        return w.get(name)
    return getattr(w, name, None)

def evaluate(op, x, y=None):
    if y is None:
        if isinstance(op, dict):
            return op[x]
        return op(x)
    else:
        if isinstance(op, dict):
            return op[(x, y)]
        return op(x, y)

def get_zero(R, add_R):
    for z in R:
        is_z = True
        for x in R:
            if evaluate(add_R, z, x) != x or evaluate(add_R, x, z) != x:
                is_z = False
                break
        if is_z:
            return z
    return None

def is_ring(R, add_R, mul_R):
    R_set = set(R)
    zero_R = get_zero(R, add_R)
    if zero_R is None: 
        return False
    
    for a in R_set:
        for b in R_set:
            if evaluate(add_R, a, b) not in R_set: return False
            if evaluate(mul_R, a, b) not in R_set: return False
            
        has_inv = False
        for b in R_set:
            if evaluate(add_R, a, b) == zero_R and evaluate(add_R, b, a) == zero_R:
                has_inv = True
                break
        if not has_inv: 
            return False
        
        for b in R_set:
            if evaluate(add_R, a, b) != evaluate(add_R, b, a): 
                return False
            for c in R_set:
                if evaluate(add_R, evaluate(add_R, a, b), c) != evaluate(add_R, a, evaluate(add_R, b, c)): 
                    return False
                if evaluate(mul_R, evaluate(mul_R, a, b), c) != evaluate(mul_R, a, evaluate(mul_R, b, c)): 
                    return False
                if evaluate(mul_R, a, evaluate(add_R, b, c)) != evaluate(add_R, evaluate(mul_R, a, b), evaluate(mul_R, a, c)): 
                    return False
                if evaluate(mul_R, evaluate(add_R, a, b), c) != evaluate(add_R, evaluate(mul_R, a, c), evaluate(mul_R, b, c)): 
                    return False
    return True

def is_ideal(N, R, add_R, mul_R, zero_R):
    N_set = set(N)
    if zero_R not in N_set:
        return False
    for x in N_set:
        for y in N_set:
            if evaluate(add_R, x, y) not in N_set:
                return False
        has_inv = False
        for y in N_set:
            if evaluate(add_R, x, y) == zero_R and evaluate(add_R, y, x) == zero_R:
                has_inv = True
                break
        if not has_inv:
            return False
    for n in N_set:
        for r in R:
            if evaluate(mul_R, n, r) not in N_set:
                return False
            if evaluate(mul_R, r, n) not in N_set:
                return False
    return True

def generate_ideal(generators, R, add_R, mul_R, zero_R):
    N = set(generators)
    N.add(zero_R)
    R_set = set(R)
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for a in N:
            for y in R_set:
                if evaluate(add_R, a, y) == zero_R and evaluate(add_R, y, a) == zero_R:
                    if y not in N and y not in new_elements:
                        new_elements.add(y)
                    break
            for b in N:
                s = evaluate(add_R, a, b)
                if s not in N and s not in new_elements:
                    new_elements.add(s)
            for r in R_set:
                p1 = evaluate(mul_R, a, r)
                if p1 not in N and p1 not in new_elements:
                    new_elements.add(p1)
                p2 = evaluate(mul_R, r, a)
                if p2 not in N and p2 not in new_elements:
                    new_elements.add(p2)
        if new_elements:
            N.update(new_elements)
            changed = True
    return N

def is_maximal_ideal(M, R, add_R, mul_R, zero_R):
    if not is_ideal(M, R, add_R, mul_R, zero_R):
        return False
    M_set = set(M)
    R_set = set(R)
    if M_set == R_set:
        return False
    for x in R_set - M_set:
        gen = M_set | {x}
        N = generate_ideal(gen, R, add_R, mul_R, zero_R)
        if N != R_set:
            return False
    return True

def conditions(witness):
    try:
        R = get_attr(witness, 'R')
        S = get_attr(witness, 'S')
        add_R = get_attr(witness, 'add_R')
        mul_R = get_attr(witness, 'mul_R')
        add_S = get_attr(witness, 'add_S')
        mul_S = get_attr(witness, 'mul_S')
        f = get_attr(witness, 'f')
        
        if not is_ring(R, add_R, mul_R):
            h1_ok = False
        elif not is_ring(S, add_S, mul_S):
            h1_ok = False
        else:
            h1_ok = True
            for x in R:
                for y in R:
                    sum_R = evaluate(add_R, x, y)
                    prod_R = evaluate(mul_R, x, y)
                    f_x = evaluate(f, x)
                    f_y = evaluate(f, y)
                    if evaluate(f, sum_R) != evaluate(add_S, f_x, f_y):
                        h1_ok = False
                        break
                    if evaluate(f, prod_R) != evaluate(mul_S, f_x, f_y):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
            if h1_ok:
                f_image = set(evaluate(f, x) for x in R)
                if f_image != set(S):
                    h1_ok = False
    except Exception:
        h1_ok = False

    try:
        S = get_attr(witness, 'S')
        add_S = get_attr(witness, 'add_S')
        mul_S = get_attr(witness, 'mul_S')
        M = get_attr(witness, 'M')
        zero_S = get_zero(S, add_S)
        if zero_S is None:
            h2_ok = False
        else:
            h2_ok = is_maximal_ideal(M, S, add_S, mul_S, zero_S)
    except Exception:
        h2_ok = False

    try:
        R = get_attr(witness, 'R')
        add_R = get_attr(witness, 'add_R')
        mul_R = get_attr(witness, 'mul_R')
        f = get_attr(witness, 'f')
        M = get_attr(witness, 'M')
        
        M_set = set(M)
        preimage = [x for x in R if evaluate(f, x) in M_set]
        
        zero_R = get_zero(R, add_R)
        if zero_R is None:
            neg_q_ok = False
        else:
            is_max = is_maximal_ideal(preimage, R, add_R, mul_R, zero_R)
            neg_q_ok = not is_max
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: M is a maximal ideal of S",
    "¬Q: The preimage of M under f is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2