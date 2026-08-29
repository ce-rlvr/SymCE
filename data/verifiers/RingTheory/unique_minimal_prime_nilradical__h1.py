import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_ring_ops(witness):
    """
    Extracts elements and operations from various possible witness formats,
    and returns an integer-mapped representation for fast, hashable operations.
    """
    if isinstance(witness, tuple) and len(witness) == 3 and callable(witness[1]) and callable(witness[2]):
        raw_elements = list(witness[0])
        raw_add = witness[1]
        raw_mul = witness[2]
    elif isinstance(witness, tuple) and len(witness) == 3:
        raw_elements = list(witness[0])
        add_t = witness[1]
        mul_t = witness[2]
        if isinstance(add_t, dict):
            def raw_add(x, y): return add_t[x][y]
            def raw_mul(x, y): return mul_t[x][y]
        else:
            def raw_add(x, y):
                idx_x = raw_elements.index(x)
                idx_y = raw_elements.index(y)
                res = add_t[idx_x][idx_y]
                if res in raw_elements: return res
                if isinstance(res, int) and 0 <= res < len(raw_elements): return raw_elements[res]
                return res
            def raw_mul(x, y):
                idx_x = raw_elements.index(x)
                idx_y = raw_elements.index(y)
                res = mul_t[idx_x][idx_y]
                if res in raw_elements: return res
                if isinstance(res, int) and 0 <= res < len(raw_elements): return raw_elements[res]
                return res
    elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        raw_elements = list(witness.elements)
        raw_add = witness.add
        raw_mul = witness.mul
    elif isinstance(witness, (list, set, tuple)):
        raw_elements = list(witness)
        def raw_add(x, y): return x + y
        def raw_mul(x, y): return x * y
    else:
        raise ValueError("Unknown witness format")

    # Remove duplicates safely
    unique_elements = []
    for e in raw_elements:
        is_dup = False
        for u in unique_elements:
            try:
                if e == u:
                    is_dup = True
                    break
            except Exception:
                pass
        if not is_dup:
            unique_elements.append(e)
    raw_elements = unique_elements
    n = len(raw_elements)

    def find_idx(val):
        for i, e in enumerate(raw_elements):
            try:
                if e == val: return i
            except Exception: pass
        for i, e in enumerate(raw_elements):
            try:
                if e.as_immutable() == val or e == val.as_immutable(): return i
            except Exception: pass
        for i, e in enumerate(raw_elements):
            try:
                if list(e) == list(val): return i
            except Exception: pass
        raise ValueError(f"Value {val} not in elements")

    add_table = [[0]*n for _ in range(n)]
    mul_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            add_table[i][j] = find_idx(raw_add(raw_elements[i], raw_elements[j]))
            mul_table[i][j] = find_idx(raw_mul(raw_elements[i], raw_elements[j]))

    zero_idx = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero_idx = i
            break
    if zero_idx is None:
        raise ValueError("No zero element found")

    elements = list(range(n))
    return elements, add_table, mul_table, zero_idx

def principal_ideal(elements, add_table, mul_table, a):
    I = {a}
    while True:
        new_I = set(I)
        for x in I:
            for y in I:
                new_I.add(add_table[x][y])
            for r in elements:
                new_I.add(mul_table[r][x])
                new_I.add(mul_table[x][r])
        if len(new_I) == len(I):
            break
        I = new_I
    return I

def get_all_ideals(elements, add_table, mul_table, zero):
    principal_ideals = [frozenset(principal_ideal(elements, add_table, mul_table, a)) for a in elements]
    ideals = set(principal_ideals)
    while True:
        new_ideals = set(ideals)
        for I in ideals:
            for P in principal_ideals:
                sum_I = {add_table[x][y] for x in I for y in P}
                new_ideals.add(frozenset(sum_I))
        if len(new_ideals) == len(ideals):
            break
        ideals = new_ideals
    return [set(I) for I in ideals]

def is_ideal(elements, add_table, mul_table, zero, I):
    if zero not in I: return False
    for x in I:
        for y in I:
            if add_table[x][y] not in I: return False
        for r in elements:
            if mul_table[r][x] not in I: return False
            if mul_table[x][r] not in I: return False
    return True

def is_prime_ideal(elements, add_table, mul_table, zero, P):
    if not is_ideal(elements, add_table, mul_table, zero, P): return False
    if len(P) == len(elements): return False
    for a in elements:
        for b in elements:
            A = principal_ideal(elements, add_table, mul_table, a)
            B = principal_ideal(elements, add_table, mul_table, b)
            contained = True
            for x in A:
                for y in B:
                    if mul_table[x][y] not in P:
                        contained = False
                        break
                if not contained: break
            if contained:
                if a not in P and b not in P:
                    return False
    return True

def get_nilpotents(elements, mul_table, zero):
    nilpotents = set()
    n = len(elements)
    for x in elements:
        curr = x
        is_nil = False
        for _ in range(n + 1):
            if curr == zero:
                is_nil = True
                break
            curr = mul_table[curr][x]
        if is_nil:
            nilpotents.add(x)
    return nilpotents

def conditions(witness):
    try:
        elements, add_table, mul_table, zero = get_ring_ops(witness)
    except Exception:
        return [False, False]
        
    try:
        ideals = get_all_ideals(elements, add_table, mul_table, zero)
        primes = []
        for I in ideals:
            if is_prime_ideal(elements, add_table, mul_table, zero, I):
                primes.append(I)
                
        minimal_primes = []
        for P in primes:
            is_minimal = True
            for Q in primes:
                if Q != P and Q.issubset(P):
                    is_minimal = False
                    break
            if is_minimal:
                minimal_primes.append(P)
                
        h1 = (len(minimal_primes) == 1)
    except Exception:
        h1 = False
        
    try:
        nilpotents = get_nilpotents(elements, mul_table, zero)
        q = is_prime_ideal(elements, add_table, mul_table, zero, nilpotents)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R has exactly one minimal prime ideal",
    "¬Q: The nilradical of R is not a prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1