import itertools
import math
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Helper functions for safe evaluation
def is_in(val, lst):
    for item in lst:
        if val == item:
            return True
    return False

def unique_elements(lst):
    res = []
    for item in lst:
        if not is_in(item, res):
            res.append(item)
    return res

def elements_equal(list1, list2):
    for item in list1:
        if not is_in(item, list2): return False
    for item in list2:
        if not is_in(item, list1): return False
    return True

def to_finite_list(iterable, max_size=50):
    if isinstance(iterable, (list, tuple, set)):
        if len(iterable) > max_size:
            raise ValueError("Iterable too large")
        return list(iterable)
    lst = []
    for i, item in enumerate(iterable):
        if i >= max_size:
            raise ValueError("Iterable too large or infinite")
        lst.append(item)
    return lst

def extract(witness, name):
    if isinstance(witness, dict):
        return witness[name]
    return getattr(witness, name)

def check_commutative_ring(R, add, mul):
    R = unique_elements(R)
    if not R: return False
    # closure and commutativity
    for a in R:
        for b in R:
            if not is_in(add(a, b), R): return False
            if not is_in(mul(a, b), R): return False
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
    # associativity and distributivity
    for a in R:
        for b in R:
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    # zero
    zeros = [z_elem for z_elem in R if all(add(z_elem, a) == a for a in R)]
    if not zeros: return False
    zero = zeros[0]
    # additive inverse
    for a in R:
        if not any(add(a, b) == zero for b in R): return False
    # identity
    ones = [u for u in R if all(mul(u, a) == a for a in R)]
    if not ones: return False
    return True

def check_ideal(R, add, mul, I):
    R = unique_elements(R)
    I = unique_elements(I)
    if not I: return False
    if not all(is_in(x_elem, R) for x_elem in I): return False
    # closure under addition
    for a in I:
        for b in I:
            if not is_in(add(a, b), I): return False
    # additive inverse
    zeros = [z_elem for z_elem in R if all(add(z_elem, a) == a for a in R)]
    if not zeros: return False
    zero = zeros[0]
    for a in I:
        inv = [b for b in R if add(a, b) == zero]
        if not any(is_in(i_elem, I) for i_elem in inv): return False
    # absorption
    for r in R:
        for x_elem in I:
            if not is_in(mul(r, x_elem), I): return False
    return True

def conditions(witness) -> list[bool]:
    try:
        R = to_finite_list(extract(witness, 'R'))
        S = to_finite_list(extract(witness, 'S'))
        R_add = extract(witness, 'R_add')
        R_mul = extract(witness, 'R_mul')
        S_add = extract(witness, 'S_add')
        S_mul = extract(witness, 'S_mul')
        I = to_finite_list(extract(witness, 'I'))
        J = to_finite_list(extract(witness, 'J'))
        f = extract(witness, 'f')
        
        if isinstance(f, dict):
            f_func = lambda x_elem: f[x_elem]
        else:
            f_func = f
            
        # Verify f maps R to S
        for x_elem in R:
            if not is_in(f_func(x_elem), S):
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R and S are commutative rings
    try:
        h1_ok = check_commutative_ring(R, R_add, R_mul) and check_commutative_ring(S, S_add, S_mul)
    except Exception:
        h1_ok = False

    # H2: I and J are ideals of R such that I + J = R
    try:
        h2_ok = False
        if check_ideal(R, R_add, R_mul, I) and check_ideal(R, R_add, R_mul, J):
            sum_IJ = []
            for i_elem in I:
                for j_elem in J:
                    sum_IJ.append(R_add(i_elem, j_elem))
            if elements_equal(unique_elements(sum_IJ), R):
                h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The images f(I) and f(J) are coprime ideals in S, meaning f(I) + f(J) = S
    try:
        f_I = unique_elements([f_func(x_elem) for x_elem in I])
        f_J = unique_elements([f_func(x_elem) for x_elem in J])
        
        is_fI_ideal = check_ideal(S, S_add, S_mul, f_I)
        is_fJ_ideal = check_ideal(S, S_add, S_mul, f_J)
        
        if not (is_fI_ideal and is_fJ_ideal):
            neg_q = True
        else:
            sum_fIfJ = []
            for i_elem in f_I:
                for j_elem in f_J:
                    sum_fIfJ.append(S_add(i_elem, j_elem))
            if elements_equal(unique_elements(sum_fIfJ), S):
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: I and J are ideals of R such that I + J = R",
    "¬Q: The images f(I) and f(J) are not coprime ideals in S"
]

N_HYP = 2
NEG_Q_INDEX = 2