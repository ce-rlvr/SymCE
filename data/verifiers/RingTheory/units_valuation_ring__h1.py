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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

_MISSING = object()

def extract(witness, key, default=_MISSING):
    if isinstance(witness, dict):
        res = witness.get(key, default)
    else:
        res = getattr(witness, key, default)
    if res is _MISSING:
        raise KeyError(f"Missing key/attribute: {key}")
    return res

def evaluate(fn, *args):
    if isinstance(fn, dict):
        if len(args) == 1:
            return fn[args[0]]
        return fn[args]
    return fn(*args)

def conditions(witness) -> list[bool]:
    # H1: v is a valuation on K with value group Gamma
    try:
        K = extract(witness, 'K')
        zero = extract(witness, 'zero')
        add = extract(witness, 'add')
        mul = extract(witness, 'mul')
        v = extract(witness, 'v')
        
        h1 = True
        K_times = [x for x in K if x != zero]
        for x in K_times:
            for y in K_times:
                xy = evaluate(mul, x, y)
                if xy != zero:
                    if evaluate(v, xy) != evaluate(v, x) + evaluate(v, y):
                        h1 = False
                        break
                x_plus_y = evaluate(add, x, y)
                if x_plus_y != zero:
                    if not (evaluate(v, x_plus_y) >= min(evaluate(v, x), evaluate(v, y))):
                        h1 = False
                        break
            if not h1:
                break
    except Exception:
        h1 = False

    # H2: R is the valuation ring associated with v
    try:
        K = extract(witness, 'K')
        zero = extract(witness, 'zero')
        v = extract(witness, 'v')
        R = extract(witness, 'R')
        gamma_zero = extract(witness, 'gamma_zero', 0)
        
        expected_R = [zero]
        for x in K:
            if x != zero:
                if evaluate(v, x) >= gamma_zero:
                    expected_R.append(x)
                    
        h2 = True
        for x in expected_R:
            if x not in R:
                h2 = False
                break
        if h2:
            for x in R:
                if x not in expected_R:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H3: u is a non-zero element of R
    try:
        u = extract(witness, 'u')
        zero = extract(witness, 'zero')
        R = extract(witness, 'R')
        
        h3 = (u != zero) and (u in R)
    except Exception:
        h3 = False

    # neg_Q: u is a unit in R if and only if v(u) = 0 (must fail)
    try:
        u = extract(witness, 'u')
        v = extract(witness, 'v')
        R = extract(witness, 'R')
        one = extract(witness, 'one')
        mul = extract(witness, 'mul')
        gamma_zero = extract(witness, 'gamma_zero', 0)
        
        is_unit = False
        for x in R:
            if evaluate(mul, u, x) == one and evaluate(mul, x, u) == one:
                is_unit = True
                break
                
        v_is_zero = (evaluate(v, u) == gamma_zero)
        
        neg_q = (is_unit != v_is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: v is a valuation on K with value group Gamma",
    "H_2: R is the valuation ring associated with v",
    "H_3: u is a non-zero element of R",
    "¬Q: u is a unit in R if and only if v(u) = 0 fails"
]

N_HYP = 3
NEG_Q_INDEX = 3