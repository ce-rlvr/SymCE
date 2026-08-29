import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z

def get_field(witness, field):
    if isinstance(witness, dict):
        return witness.get(field)
    return getattr(witness, field, None)

def check_comm_ring_with_id(elements, add, mul, zero, one):
    if zero not in elements or one not in elements: 
        return False
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: 
            return False
        if mul(a, one) != a or mul(one, a) != a: 
            return False
        
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
            
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    return True

def check_integral_extension(R, S, add, mul, zero, one_R):
    for x in S:
        M = []
        for r in R:
            val = mul(r, one_R)
            if val not in M:
                M.append(val)
        
        x_power = one_R
        integral = False
        for n in range(1, len(S) + 2):
            x_power = mul(x_power, x)
            term = mul(one_R, x_power)
            if term in M:
                integral = True
                break
            new_M = list(M)
            for r in R:
                rx = mul(r, x_power)
                for m in M:
                    val = add(m, rx)
                    if val not in new_M:
                        new_M.append(val)
            M = new_M
        if not integral:
            return False
    return True

def is_prime_ideal(Q, S, add, mul, zero):
    if not Q: return False
    if len(Q) == len(S): return False
    if zero not in Q: return False
    for q1 in Q:
        for q2 in Q:
            if add(q1, q2) not in Q: return False
    for q in Q:
        for s in S:
            if mul(s, q) not in Q: return False
            if mul(q, s) not in Q: return False
    for a in S:
        for b in S:
            if mul(a, b) in Q:
                if a not in Q and b not in Q:
                    return False
    return True

def check_P_eq_Q_cap_R(P, Q, R):
    expected_P = [x for x in R if x in Q]
    if len(P) != len(expected_P): return False
    for x in P:
        if x not in expected_P: return False
    return True

def is_maximal_ideal(I, A, add, mul, zero, one):
    if len(I) == len(A): return False
    if zero not in I: return False
    for i1 in I:
        for i2 in I:
            if add(i1, i2) not in I: return False
    for i in I:
        for a in A:
            if mul(a, i) not in I: return False
            if mul(i, a) not in I: return False
            
    for a in A:
        if a in I: continue
        has_inv = False
        for b in A:
            ab = mul(a, b)
            coset = [add(ab, i) for i in I]
            if one in coset:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 9:
            R, S, add, mul, zero, one_R, one_S, Q, P = witness
        else:
            R = get_field(witness, 'R')
            S = get_field(witness, 'S')
            add = get_field(witness, 'add')
            mul = get_field(witness, 'mul')
            zero = get_field(witness, 'zero')
            one_R = get_field(witness, 'one_R')
            one_S = get_field(witness, 'one_S')
            Q = get_field(witness, 'Q')
            P = get_field(witness, 'P')
            
        if any(v is None for v in [R, S, add, mul, zero, one_R, one_S, Q, P]):
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        h1 = check_comm_ring_with_id(R, add, mul, zero, one_R) and \
             check_comm_ring_with_id(S, add, mul, zero, one_S)
    except Exception:
        h1 = False

    try:
        if any(x not in S for x in R):
            h2 = False
        else:
            h2 = check_integral_extension(R, S, add, mul, zero, one_R)
    except Exception:
        h2 = False

    try:
        h3 = is_prime_ideal(Q, S, add, mul, zero)
    except Exception:
        h3 = False

    try:
        h4 = check_P_eq_Q_cap_R(P, Q, R)
    except Exception:
        h4 = False

    try:
        q_max = is_maximal_ideal(Q, S, add, mul, zero, one_S)
        p_max = is_maximal_ideal(P, R, add, mul, zero, one_R)
        neg_q = not (q_max == p_max)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: S is an integral extension of R",
    "H_3: Q is a prime ideal of S",
    "H_4: P = Q ∩ R",
    "¬Q: Q is a maximal ideal of S if and only if P is a maximal ideal of R is FALSE"
]

N_HYP = 4
NEG_Q_INDEX = 4