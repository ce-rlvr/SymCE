import itertools
import functools
import math
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 7:
        return witness
    if isinstance(witness, dict):
        return (
            witness['elements'],
            witness['add'],
            witness['mul'],
            witness['zero'],
            witness['I'],
            witness['J'],
            witness['K']
        )
    return (
        getattr(witness, 'elements'),
        getattr(witness, 'add'),
        getattr(witness, 'mul'),
        getattr(witness, 'zero'),
        getattr(witness, 'I'),
        getattr(witness, 'J'),
        getattr(witness, 'K')
    )

def make_callable(func_or_dict):
    if isinstance(func_or_dict, dict):
        return lambda a, b: func_or_dict[(a, b)]
    return func_or_dict

def check_ring(elements, add, mul, zero):
    if zero not in elements: 
        return False
    # closure
    for a in elements:
        for b in elements:
            try:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
            except Exception:
                return False
    # commutativity of add
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
    # associativity of add and mul, distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    # identity of add
    for a in elements:
        if add(a, zero) != a: return False
    # inverse of add
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
    return True

def check_ideal(elements, add, mul, zero, S):
    S = list(S)
    if not S: return False
    if zero not in S: return False
    for e in S:
        if e not in elements: return False
    # subgroup under add
    for a in S:
        for b in S:
            if add(a, b) not in S: return False
        has_inv = False
        for b in S:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
    # absorb mul (two-sided ideal)
    for s in S:
        for r in elements:
            if mul(s, r) not in S: return False
            if mul(r, s) not in S: return False
    return True

def check_comaximal(elements, add, I, J):
    sums = []
    for i in I:
        for j in J:
            try:
                sums.append(add(i, j))
            except Exception:
                return False
    for e in elements:
        if e not in sums:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        elements, add_func, mul_func, zero, I, J, K = extract_witness(witness)
        elements = list(elements)
        
        # Restrict to finite rings to ensure the verifier runs quickly
        if len(elements) > 100:
            return [False, False, False, False]
            
        add = make_callable(add_func)
        mul = make_callable(mul_func)
        I = list(I)
        J = list(J)
        K = list(K)
        
        h1 = check_ring(elements, add, mul, zero)
        if not h1:
            return [False, False, False, False]
            
        h2 = check_ideal(elements, add, mul, zero, I) and check_ideal(elements, add, mul, zero, J)
        h3 = all(k in I for k in K) and all(k in J for k in K)
        
        lhs = check_comaximal(elements, add, I, J)
        k_is_ideal = check_ideal(elements, add, mul, zero, K)
        
        # The conclusion Q is: LHS <==> (K is an ideal and I/K + J/K == R/K)
        # If K is an ideal, RHS is equivalent to LHS (by the Correspondence Theorem).
        # If K is not an ideal, RHS is invalid/False (R/K is not a quotient ring).
        # So Q is True iff (K is an ideal) or (not LHS).
        # Thus neg_Q is True iff LHS is True AND K is not an ideal.
        neg_q = lhs and not k_is_ideal
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are ideals of R",
    "H_3: I and J both contain K",
    "¬Q: I and J are comaximal in R, but K is not an ideal (so R/K is not a quotient ring)"
]

N_HYP = 3
NEG_Q_INDEX = 3