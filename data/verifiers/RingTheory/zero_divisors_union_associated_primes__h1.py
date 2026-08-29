import itertools
import math
import functools
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: I is a proper ideal of R",
    "H_3: I = q_1 \\cap ... \\cap q_n is an irredundant primary decomposition of I",
    "H_4: P_i = \\sqrt{q_i} for i = 1, ..., n are the associated primes of I",
    "¬Q: The set of zero divisors on R/I is not equal to the union of the associated primes P_1 \\cup ... \\cup P_n"
]

N_HYP = 4
NEG_Q_INDEX = 4

def is_ring(R, add, mul, zero):
    if zero not in R: return False
    for a in R:
        if add(a, zero) != a or add(zero, a) != a: return False
        if not any(add(a, b) == zero and add(b, a) == zero for b in R): return False
    for a in R:
        for b in R:
            if add(a, b) not in R: return False
            if mul(a, b) not in R: return False
            if add(a, b) != add(b, a): return False
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def is_ideal(R, add, mul, zero, I):
    if not I: return False
    if zero not in I: return False
    for a in I:
        for b in I:
            if add(a, b) not in I: return False
        if not any(add(a, b) == zero for b in I): return False
    for r in R:
        for a in I:
            if mul(r, a) not in I: return False
            if mul(a, r) not in I: return False
    return True

def ideal_generated_by(R, add, mul, y):
    products = set(mul(r1, mul(y, r2)) for r1 in R for r2 in R)
    closure = list(products)
    changed = True
    while changed:
        changed = False
        n = len(closure)
        for i in range(n):
            for j in range(i, n):
                s = add(closure[i], closure[j])
                if s not in closure:
                    closure.append(s)
                    changed = True
    return set(closure)

def is_ideal_nilpotent_mod(R, add, mul, I_gen, Q):
    current_I = set(I_gen)
    for _ in range(len(R)):
        if current_I.issubset(set(Q)):
            return True
        products = set(mul(a, b) for a in current_I for b in I_gen)
        closure = list(products)
        changed = True
        while changed:
            changed = False
            n = len(closure)
            for i in range(n):
                for j in range(i, n):
                    s = add(closure[i], closure[j])
                    if s not in closure:
                        closure.append(s)
                        changed = True
        current_I = set(closure)
    return current_I.issubset(set(Q))

def is_primary_nc(R, add, mul, zero, Q):
    if not is_ideal(R, add, mul, zero, Q): return False
    if set(Q) == set(R): return False
    for x in R:
        if x in Q: continue
        for y in R:
            if all(mul(x, mul(r, y)) in Q for r in R):
                I_y = ideal_generated_by(R, add, mul, y)
                if not is_ideal_nilpotent_mod(R, add, mul, I_y, Q):
                    return False
    return True

def is_prime_ideal(R, add, mul, zero, P):
    if not is_ideal(R, add, mul, zero, P): return False
    if set(P) == set(R): return False
    for x in R:
        if x in P: continue
        for y in R:
            if y in P: continue
            if all(mul(x, mul(r, y)) in P for r in R):
                return False
    return True

def is_prime_radical(R, add, mul, zero, P, Q):
    if not is_prime_ideal(R, add, mul, zero, P): return False
    if not set(Q).issubset(set(P)): return False
    return is_ideal_nilpotent_mod(R, add, mul, P, Q)

def is_associated_prime(R, mul, I, P):
    for x in R:
        if x in I: continue
        ann = set(r for r in R if mul(r, x) in I)
        if ann == set(P): return True
        ann_r = set(r for r in R if mul(x, r) in I)
        if ann_r == set(P): return True
        ann_2 = set(r for r in R if all(mul(r, mul(s, x)) in I for s in R))
        if ann_2 == set(P): return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            I = witness['I']
            q_list = witness['q_list']
            P_list = witness['P_list']
        elif isinstance(witness, tuple):
            R, add, mul, zero, I, q_list, P_list = witness
        else:
            R = witness.R
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            I = witness.I
            q_list = witness.q_list
            P_list = witness.P_list
    except Exception:
        return [False] * 5

    # H1
    try:
        h1 = False
        if isinstance(R, (list, tuple, set)) and len(R) > 0:
            h1 = is_ring(R, add, mul, zero)
    except Exception:
        h1 = False

    # H2
    try:
        h2 = False
        if h1 and set(I) != set(R):
            h2 = is_ideal(R, add, mul, zero, I)
    except Exception:
        h2 = False

    # H3
    try:
        h3 = False
        if h1 and h2 and q_list:
            intersect = set(R)
            for q in q_list:
                intersect = intersect.intersection(set(q))
            if intersect == set(I):
                irredundant = True
                for i in range(len(q_list)):
                    sub_intersect = set(R)
                    for j in range(len(q_list)):
                        if i != j:
                            sub_intersect = sub_intersect.intersection(set(q_list[j]))
                    if sub_intersect == set(I):
                        irredundant = False
                        break
                if irredundant:
                    all_primary = True
                    for q in q_list:
                        if not is_primary_nc(R, add, mul, zero, q):
                            all_primary = False
                            break
                    h3 = all_primary
    except Exception:
        h3 = False

    # H4
    try:
        h4 = False
        if h1 and h2 and len(q_list) == len(P_list):
            P_sets = [frozenset(P) for P in P_list]
            if len(set(P_sets)) == len(P_list):
                all_match = True
                for q, P in zip(q_list, P_list):
                    if not is_prime_radical(R, add, mul, zero, P, q):
                        all_match = False
                        break
                    if not is_associated_prime(R, mul, I, P):
                        all_match = False
                        break
                h4 = all_match
    except Exception:
        h4 = False

    # neg_Q
    try:
        neg_q = False
        if h1 and h2:
            union_P = set()
            for P in P_list:
                union_P.update(P)
                
            zero_divisors = set()
            for x in R:
                is_zd = False
                for y in R:
                    if y not in I:
                        if mul(x, y) in I or mul(y, x) in I:
                            is_zd = True
                            break
                if is_zd:
                    zero_divisors.add(x)
                    
            neg_q = (zero_divisors != union_P)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]