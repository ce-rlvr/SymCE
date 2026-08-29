import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def get_op(witness, name, default=None):
    if isinstance(witness, dict):
        return witness.get(name, default)
    return getattr(witness, name, default)

def apply_f(f, val):
    if isinstance(f, dict):
        return f.get(val)
    return f(val)

def apply_binop(op, a, b, default_op):
    if op is None:
        return default_op(a, b)
    if isinstance(op, dict):
        return op.get((a, b))
    return op(a, b)

def conditions(witness) -> list[bool]:
    R = get_op(witness, 'R', None)
    add_R = get_op(witness, 'add_R', None)
    mul_R = get_op(witness, 'mul_R', None)
    add_S = get_op(witness, 'add_S', None)
    mul_S = get_op(witness, 'mul_S', None)
    f = get_op(witness, 'f', None)
    x = get_op(witness, 'x', None)
    y = get_op(witness, 'y', None)
    zero_R = get_op(witness, 'zero_R', 0)
    zero_S = get_op(witness, 'zero_S', 0)

    def _add_R(a, b): return apply_binop(add_R, a, b, lambda u, v: u + v)
    def _mul_R(a, b): return apply_binop(mul_R, a, b, lambda u, v: u * v)
    def _add_S(a, b): return apply_binop(add_S, a, b, lambda u, v: u + v)
    def _mul_S(a, b): return apply_binop(mul_S, a, b, lambda u, v: u * v)
    def _f(a): return apply_f(f, a)

    # H1: f is a ring homomorphism
    h1_ok = False
    try:
        if f is not None:
            h1_ok = True
            elements_to_check = list(R) if R is not None else [x, y, zero_R]
            for a in elements_to_check:
                for b in elements_to_check:
                    if _f(_add_R(a, b)) != _add_S(_f(a), _f(b)):
                        h1_ok = False
                        break
                    if _f(_mul_R(a, b)) != _mul_S(_f(a), _f(b)):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H2: x, y are orthogonal idempotents
    h2_ok = False
    try:
        if x is not None and y is not None:
            if _mul_R(x, x) == x and _mul_R(y, y) == y:
                if _mul_R(x, y) == zero_R and _mul_R(y, x) == zero_R:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: f(x) and f(y) are NOT orthogonal idempotents in S
    neg_q = False
    try:
        if f is not None and x is not None and y is not None:
            fx = _f(x)
            fy = _f(y)
            q_ok = (_mul_S(fx, fx) == fx) and \
                   (_mul_S(fy, fy) == fy) and \
                   (_mul_S(fx, fy) == zero_S) and \
                   (_mul_S(fy, fx) == zero_S)
            neg_q = not q_ok
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism",
    "H_2: x, y in R are orthogonal idempotents",
    "¬Q: f(x) and f(y) are not orthogonal idempotents in S"
]

N_HYP = 2
NEG_Q_INDEX = 2