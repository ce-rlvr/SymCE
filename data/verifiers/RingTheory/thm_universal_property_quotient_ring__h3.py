import sympy
from sympy import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_val(table, i, j):
    if callable(table):
        return table(i, j)
    return table[i][j]

def get_f(f, x):
    if callable(f):
        return f(x)
    return f[x]

def get_attr_or_key(obj, key):
    if isinstance(obj, dict):
        return obj[key]
    return getattr(obj, key)

def is_ring(elements, add, mul):
    if not elements: 
        return False
    # check closure
    for i in elements:
        for j in elements:
            try:
                if get_val(add, i, j) not in elements: return False
                if get_val(mul, i, j) not in elements: return False
            except Exception:
                return False
    # check add associativity
    for i in elements:
        for j in elements:
            for k in elements:
                if get_val(add, get_val(add, i, j), k) != get_val(add, i, get_val(add, j, k)): return False
    # check add commutativity
    for i in elements:
        for j in elements:
            if get_val(add, i, j) != get_val(add, j, i): return False
    # check add identity
    id_add = None
    for i in elements:
        if all(get_val(add, i, j) == j and get_val(add, j, i) == j for j in elements):
            id_add = i
            break
    if id_add is None: 
        return False
    # check add inverse
    for i in elements:
        if not any(get_val(add, i, j) == id_add and get_val(add, j, i) == id_add for j in elements): return False
    # check mul associativity
    for i in elements:
        for j in elements:
            for k in elements:
                if get_val(mul, get_val(mul, i, j), k) != get_val(mul, i, get_val(mul, j, k)): return False
    # check distributivity
    for i in elements:
        for j in elements:
            for k in elements:
                if get_val(mul, i, get_val(add, j, k)) != get_val(add, get_val(mul, i, j), get_val(mul, i, k)): return False
                if get_val(mul, get_val(add, i, j), k) != get_val(add, get_val(mul, i, k), get_val(mul, j, k)): return False
    return True

def is_hom(elements_R, add_R, mul_R, elements_S, add_S, mul_S, f):
    for i in elements_R:
        for j in elements_R:
            try:
                if get_f(f, get_val(add_R, i, j)) != get_val(add_S, get_f(f, i), get_f(f, j)): return False
                if get_f(f, get_val(mul_R, i, j)) != get_val(mul_S, get_f(f, i), get_f(f, j)): return False
            except Exception:
                return False
    return True

def is_subset_ker(elements_R, elements_S, add_S, f, I):
    id_add_S = None
    for i in elements_S:
        if all(get_val(add_S, i, j) == j and get_val(add_S, j, i) == j for j in elements_S):
            id_add_S = i
            break
    if id_add_S is None: 
        return False
    for x in I:
        if x not in elements_R: 
            return False
        try:
            if get_f(f, x) != id_add_S: 
                return False
        except Exception:
            return False
    return True

def is_ideal(elements_R, add_R, mul_R, I):
    if not I: 
        return False
    for x in I:
        if x not in elements_R: 
            return False
    id_add_R = None
    for i in elements_R:
        if all(get_val(add_R, i, j) == j and get_val(add_R, j, i) == j for j in elements_R):
            id_add_R = i
            break
    if id_add_R not in I: 
        return False
    # check closure under addition
    for i in I:
        for j in I:
            if get_val(add_R, i, j) not in I: return False
    # check closure under additive inverse
    for i in I:
        inv_i = None
        for j in elements_R:
            if get_val(add_R, i, j) == id_add_R and get_val(add_R, j, i) == id_add_R:
                inv_i = j
                break
        if inv_i not in I: return False
    # check ideal property (absorbs multiplication)
    for i in I:
        for r in elements_R:
            if get_val(mul_R, i, r) not in I: return False
            if get_val(mul_R, r, i) not in I: return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 8:
            R, S, add_R, mul_R, add_S, mul_S, f, I = witness
        else:
            R = get_attr_or_key(witness, "R")
            S = get_attr_or_key(witness, "S")
            add_R = get_attr_or_key(witness, "add_R")
            mul_R = get_attr_or_key(witness, "mul_R")
            add_S = get_attr_or_key(witness, "add_S")
            mul_S = get_attr_or_key(witness, "mul_S")
            f = get_attr_or_key(witness, "f")
            I = get_attr_or_key(witness, "I")
            
        R = list(R)
        S = list(S)
        I = list(I)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_ring(R, add_R, mul_R) and is_ring(S, add_S, mul_S)
    except Exception:
        h1 = False

    try:
        h2 = is_hom(R, add_R, mul_R, S, add_S, mul_S, f)
    except Exception:
        h2 = False

    try:
        h3 = is_subset_ker(R, S, add_S, f, I)
    except Exception:
        h3 = False

    try:
        neg_q = not is_ideal(R, add_R, mul_R, I)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism",
    "H_3: I is a subset of ker(f)",
    "¬Q: R/I is not a valid quotient ring (I is not an ideal)"
]

N_HYP = 3
NEG_Q_INDEX = 3