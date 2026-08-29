import sympy
from sympy import *
import itertools
import functools
import math

# Top-level setup
x, y, z = sympy.symbols('x y z')

def parse_witness(witness):
    if isinstance(witness, dict):
        R = witness['R']
        I = witness['I']
        J = witness['J']
        n = witness['n']
        add = witness.get('add', lambda a, b: a + b)
        mul = witness.get('mul', lambda a, b: a * b)
        return R, add, mul, I, J, n
    elif isinstance(witness, tuple) or isinstance(witness, list):
        if len(witness) == 6:
            return witness[0], witness[1], witness[2], witness[3], witness[4], witness[5]
        elif len(witness) == 4:
            return witness[0], lambda a, b: a + b, lambda a, b: a * b, witness[1], witness[2], witness[3]
    else:
        R = witness.R
        I = witness.I
        J = witness.J
        n = witness.n
        add = getattr(witness, 'add', lambda a, b: a + b)
        mul = getattr(witness, 'mul', lambda a, b: a * b)
        return R, add, mul, I, J, n

def check_ring(R, add, mul):
    R = list(R)
    if not R: return False
    # Check closure
    for a in R:
        for b in R:
            if add(a, b) not in R: return False
            if mul(a, b) not in R: return False
    # Check associativity of add
    for a in R:
        for b in R:
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
    # Check commutativity of add
    for a in R:
        for b in R:
            if add(a, b) != add(b, a): return False
    # Find zero
    zeros = []
    for z_elem in R:
        if all(add(z_elem, a) == a and add(a, z_elem) == a for a in R):
            zeros.append(z_elem)
    if not zeros: return False
    zero = zeros[0]
    # Check inverses
    for a in R:
        if not any(add(a, b) == zero and add(b, a) == zero for b in R):
            return False
    # Check associativity of mul
    for a in R:
        for b in R:
            for c in R:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
    # Check distributivity
    for a in R:
        for b in R:
            for c in R:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def check_I_plus_J_eq_R(R, add, I, J):
    R = list(R)
    I = list(I)
    J = list(J)
    for elem in I:
        if elem not in R: return False
    for elem in J:
        if elem not in R: return False
    
    sums = []
    for i in I:
        for j in J:
            sums.append(add(i, j))
    
    for r in R:
        if r not in sums:
            return False
    return True

def check_n(n):
    return isinstance(n, int) and n > 0

def is_ideal(S, R, add, mul):
    S = list(S)
    if not S: return False
    # Find zero in R
    zero = None
    for z_elem in R:
        if all(add(z_elem, a) == a for a in R):
            zero = z_elem
            break
    if zero is None or zero not in S: return False
    
    # Check additive subgroup
    for a in S:
        for b in S:
            if add(a, b) not in S: return False
            
    for a in S:
        inv = None
        for b in R:
            if add(a, b) == zero:
                inv = b
                break
        if inv is None or inv not in S: return False
        
    # Check ideal property
    for s in S:
        for r in R:
            if mul(s, r) not in S: return False
            if mul(r, s) not in S: return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        R, add, mul, I, J, n = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = check_ring(R, add, mul)
    except Exception:
        h1 = False
        
    try:
        h2 = check_I_plus_J_eq_R(R, add, I, J)
    except Exception:
        h2 = False
        
    try:
        h3 = check_n(n)
    except Exception:
        h3 = False
        
    try:
        # The conclusion states that M_n(I) and M_n(J) are matrix ideals and sum to M_n(R).
        # The sum equality M_n(I) + M_n(J) = M_n(R) is mathematically guaranteed if I+J=R.
        # The conclusion fails iff M_n(I) or M_n(J) is not an ideal, which means I or J is not an ideal.
        q = is_ideal(I, R, add, mul) and is_ideal(J, R, add, mul)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I + J = R",
    "H_3: n is a positive integer",
    "¬Q: M_n(I) and M_n(J) are not both matrix ideals (i.e., I or J is not an ideal of R)"
]

N_HYP = 3
NEG_Q_INDEX = 3