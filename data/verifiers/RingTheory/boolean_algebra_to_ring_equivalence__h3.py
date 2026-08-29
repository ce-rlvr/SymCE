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
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def apply2(op, a, b):
    if callable(op): 
        return op(a, b)
    if isinstance(op, dict):
        if (a, b) in op:
            return op[(a, b)]
        else:
            return op[a][b]
    return op[a][b]

def apply1(op, a):
    if callable(op): 
        return op(a)
    if isinstance(op, dict): 
        return op[a]
    return op[a]

def extract(witness):
    if isinstance(witness, dict):
        return list(witness['B']), witness['OR'], witness['AND'], witness['NOT'], witness['ZERO'], witness['ONE'], witness['PLUS'], witness['MULT']
    elif hasattr(witness, 'B') and hasattr(witness, 'OR'):
        return list(witness.B), witness.OR, witness.AND, witness.NOT, witness.ZERO, witness.ONE, witness.PLUS, witness.MULT
    else:
        return list(witness[0]), witness[1], witness[2], witness[3], witness[4], witness[5], witness[6], witness[7]

def is_boolean_algebra(B, OR, AND, NOT, ZERO, ONE):
    if ZERO not in B or ONE not in B: 
        return False
    for a in B:
        if apply1(NOT, a) not in B: return False
        if apply2(OR, a, ZERO) != a: return False
        if apply2(OR, ZERO, a) != a: return False
        if apply2(AND, a, ONE) != a: return False
        if apply2(AND, ONE, a) != a: return False
        if apply2(OR, a, apply1(NOT, a)) != ONE: return False
        if apply2(AND, a, apply1(NOT, a)) != ZERO: return False
        for b in B:
            if apply2(OR, a, b) not in B: return False
            if apply2(AND, a, b) not in B: return False
            if apply2(OR, a, b) != apply2(OR, b, a): return False
            if apply2(AND, a, b) != apply2(AND, b, a): return False
            if apply2(OR, a, apply2(AND, a, b)) != a: return False
            if apply2(AND, a, apply2(OR, a, b)) != a: return False
            for c in B:
                if apply2(OR, a, apply2(OR, b, c)) != apply2(OR, apply2(OR, a, b), c): return False
                if apply2(AND, a, apply2(AND, b, c)) != apply2(AND, apply2(AND, a, b), c): return False
                if apply2(OR, a, apply2(AND, b, c)) != apply2(AND, apply2(OR, a, b), apply2(OR, a, c)): return False
                if apply2(AND, a, apply2(OR, b, c)) != apply2(OR, apply2(AND, a, b), apply2(AND, a, c)): return False
    return True

def is_plus_correct(B, OR, AND, NOT, PLUS):
    for a in B:
        for b in B:
            not_b = apply1(NOT, b)
            not_a = apply1(NOT, a)
            term1 = apply2(AND, a, not_b)
            term2 = apply2(AND, not_a, b)
            expected = apply2(OR, term1, term2)
            if apply2(PLUS, a, b) != expected:
                return False
    return True

def is_boolean_ring_with_identity(B, PLUS, MULT, ZERO, ONE):
    # Abelian group under PLUS
    for a in B:
        if apply2(PLUS, a, ZERO) != a: return False
        if apply2(PLUS, ZERO, a) != a: return False
        has_inv = False
        for b in B:
            if apply2(PLUS, a, b) == ZERO and apply2(PLUS, b, a) == ZERO:
                has_inv = True
                break
        if not has_inv: return False
        for b in B:
            if apply2(PLUS, a, b) not in B: return False
            if apply2(PLUS, a, b) != apply2(PLUS, b, a): return False
            for c in B:
                if apply2(PLUS, a, apply2(PLUS, b, c)) != apply2(PLUS, apply2(PLUS, a, b), c): return False
    
    # Monoid under MULT
    for a in B:
        if apply2(MULT, a, ONE) != a: return False
        if apply2(MULT, ONE, a) != a: return False
        for b in B:
            if apply2(MULT, a, b) not in B: return False
            for c in B:
                if apply2(MULT, a, apply2(MULT, b, c)) != apply2(MULT, apply2(MULT, a, b), c): return False
                
    # Distributivity
    for a in B:
        for b in B:
            for c in B:
                if apply2(MULT, a, apply2(PLUS, b, c)) != apply2(PLUS, apply2(MULT, a, b), apply2(MULT, a, c)): return False
                if apply2(MULT, apply2(PLUS, a, b), c) != apply2(PLUS, apply2(MULT, a, c), apply2(MULT, b, c)): return False
                
    # Boolean ring property
    for a in B:
        if apply2(MULT, a, a) != a: return False
        
    return True

def conditions(witness):
    try:
        B, OR, AND, NOT, ZERO, ONE, PLUS, MULT = extract(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_boolean_algebra(B, OR, AND, NOT, ZERO, ONE)
    except Exception:
        h1 = False
        
    try:
        h2 = is_plus_correct(B, OR, AND, NOT, PLUS)
    except Exception:
        h2 = False
        
    try:
        q = is_boolean_ring_with_identity(B, PLUS, MULT, ZERO, ONE)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (B, or, and, not, 0, 1) is a Boolean algebra",
    "H_2: a + b = (a and not b) or (not a and b)",
    "¬Q: (B, +, *, 0, 1) is not a Boolean ring with identity"
]

N_HYP = 2
NEG_Q_INDEX = 2