import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def evaluate(op, a, b=None):
    if b is None:
        if isinstance(op, (dict, list, tuple)):
            return op[a]
        return op(a)
    else:
        if isinstance(op, dict):
            if (a, b) in op:
                return op[(a, b)]
            else:
                return op[a][b]
        elif isinstance(op, (list, tuple)):
            return op[a][b]
        return op(a, b)

def is_ring(elements, add, mul):
    # check closure
    for a in elements:
        for b in elements:
            if evaluate(add, a, b) not in elements: return False
            if evaluate(mul, a, b) not in elements: return False
            
    # check addition associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if evaluate(add, evaluate(add, a, b), c) != evaluate(add, a, evaluate(add, b, c)): return False
                
    # check addition commutativity
    for a in elements:
        for b in elements:
            if evaluate(add, a, b) != evaluate(add, b, a): return False
            
    # check zero element
    zero = None
    for z in elements:
        if all(evaluate(add, z, a) == a for a in elements):
            zero = z
            break
    if zero is None: return False
    
    # check additive inverse
    for a in elements:
        has_inv = False
        for b in elements:
            if evaluate(add, a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    # check multiplication associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if evaluate(mul, evaluate(mul, a, b), c) != evaluate(mul, a, evaluate(mul, b, c)): return False
                
    # check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if evaluate(mul, a, evaluate(add, b, c)) != evaluate(add, evaluate(mul, a, b), evaluate(mul, a, c)): return False
                if evaluate(mul, evaluate(add, a, b), c) != evaluate(add, evaluate(mul, a, c), evaluate(mul, b, c)): return False
                
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            f = witness['f']
        elif isinstance(witness, tuple) and len(witness) == 7:
            R, S, R_add, R_mul, S_add, S_mul, f = witness
        else:
            R = witness.R
            S = witness.S
            R_add = witness.R_add
            R_mul = witness.R_mul
            S_add = witness.S_add
            S_mul = witness.S_mul
            f = witness.f
    except Exception:
        return [False, False, False, False]
        
    # H1: f is a ring homomorphism from R to S
    try:
        h1 = True
        if not is_ring(R, R_add, R_mul):
            h1 = False
        elif not is_ring(S, S_add, S_mul):
            h1 = False
        else:
            for a in R:
                if evaluate(f, a) not in S:
                    h1 = False
                    break
            if h1:
                for a in R:
                    for b in R:
                        if evaluate(f, evaluate(R_add, a, b)) != evaluate(S_add, evaluate(f, a), evaluate(f, b)):
                            h1 = False
                            break
                        if evaluate(f, evaluate(R_mul, a, b)) != evaluate(S_mul, evaluate(f, a), evaluate(f, b)):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H2: f is surjective
    try:
        image = []
        for a in R:
            val = evaluate(f, a)
            if val not in image:
                image.append(val)
        h2 = True
        for x in S:
            if x not in image:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: R is a commutative ring
    try:
        h3 = True
        for a in R:
            for b in R:
                if evaluate(R_mul, a, b) != evaluate(R_mul, b, a):
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: S is NOT commutative
    try:
        neg_q = False
        for a in S:
            for b in S:
                if evaluate(S_mul, a, b) != evaluate(S_mul, b, a):
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: f is surjective",
    "H_3: R is a commutative ring",
    "¬Q: S is not commutative"
]

N_HYP = 3
NEG_Q_INDEX = 3