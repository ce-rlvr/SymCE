import operator
import itertools
import functools
import math
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(w, name, default=None):
    if isinstance(w, dict) and name in w:
        return w[name]
    if hasattr(w, name):
        return getattr(w, name)
    return default

def contains(lst, item, eq):
    return any(eq(x, item) for x in lst)

def find_zero(ring, add, eq):
    for z in ring:
        if all(eq(add(z, x), x) and eq(add(x, z), x) for x in ring):
            return z
    return None

def is_ideal(subset, ring, add, mul, zero, eq):
    if not subset:
        return False
    for x in subset:
        if not contains(ring, x, eq):
            return False
    for x in subset:
        for y in subset:
            if not contains(subset, add(x, y), eq):
                return False
    if not contains(subset, zero, eq):
        return False
    for x in subset:
        has_inv = False
        for y in subset:
            if eq(add(x, y), zero) and eq(add(y, x), zero):
                has_inv = True
                break
        if not has_inv:
            return False
    for x in subset:
        for r in ring:
            if not contains(subset, mul(r, x), eq):
                return False
            if not contains(subset, mul(x, r), eq):
                return False
    return True

def ideal_generated_by(generators, ring, add, mul, zero, eq):
    ideal = []
    for g in generators:
        if not contains(ideal, g, eq):
            ideal.append(g)
    if not contains(ideal, zero, eq):
        ideal.append(zero)
        
    while True:
        size = len(ideal)
        new_elements = []
        for x in ideal:
            for y in ideal:
                s = add(x, y)
                if not contains(ideal, s, eq) and not contains(new_elements, s, eq):
                    new_elements.append(s)
        for x in ideal:
            for r in ring:
                p1 = mul(r, x)
                if not contains(ideal, p1, eq) and not contains(new_elements, p1, eq):
                    new_elements.append(p1)
                p2 = mul(x, r)
                if not contains(ideal, p2, eq) and not contains(new_elements, p2, eq):
                    new_elements.append(p2)
        ideal.extend(new_elements)
        if len(ideal) == size:
            break
    return ideal

def conditions(witness) -> list[bool]:
    R = get_attr(witness, 'R')
    S = get_attr(witness, 'S')
    add_R = get_attr(witness, 'add_R', operator.add)
    mul_R = get_attr(witness, 'mul_R', operator.mul)
    add_S = get_attr(witness, 'add_S', operator.add)
    mul_S = get_attr(witness, 'mul_S', operator.mul)
    eq_R = get_attr(witness, 'eq_R', operator.eq)
    eq_S = get_attr(witness, 'eq_S', operator.eq)
    f = get_attr(witness, 'f')
    I = get_attr(witness, 'I')
    J = get_attr(witness, 'J')

    if R is None or S is None or f is None or I is None or J is None:
        return [False, False, False, False]

    zero_R = get_attr(witness, 'zero_R')
    if zero_R is None:
        try:
            zero_R = find_zero(R, add_R, eq_R)
        except Exception:
            pass
    
    zero_S = get_attr(witness, 'zero_S')
    if zero_S is None:
        try:
            zero_S = find_zero(S, add_S, eq_S)
        except Exception:
            pass

    if zero_R is None or zero_S is None:
        return [False, False, False, False]

    # H1: f is a surjective ring homomorphism
    try:
        h1 = True
        for a in R:
            for b in R:
                if not eq_S(f(add_R(a, b)), add_S(f(a), f(b))):
                    h1 = False
                    break
                if not eq_S(f(mul_R(a, b)), mul_S(f(a), f(b))):
                    h1 = False
                    break
            if not h1:
                break
        
        if h1:
            f_R = []
            for a in R:
                fa = f(a)
                if not contains(f_R, fa, eq_S):
                    f_R.append(fa)
            for s in S:
                if not contains(f_R, s, eq_S):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        h2 = is_ideal(I, R, add_R, mul_R, zero_R, eq_R)
    except Exception:
        h2 = False

    # H3: J is an ideal of R
    try:
        h3 = is_ideal(J, R, add_R, mul_R, zero_R, eq_R)
    except Exception:
        h3 = False

    # neg_Q: f(IJ) != f(I)f(J)
    try:
        IJ_generators = []
        for a in I:
            for b in J:
                IJ_generators.append(mul_R(a, b))
        IJ = ideal_generated_by(IJ_generators, R, add_R, mul_R, zero_R, eq_R)
        
        f_IJ = []
        for x in IJ:
            fx = f(x)
            if not contains(f_IJ, fx, eq_S):
                f_IJ.append(fx)
                
        f_I = []
        for a in I:
            fa = f(a)
            if not contains(f_I, fa, eq_S):
                f_I.append(fa)
        f_J = []
        for b in J:
            fb = f(b)
            if not contains(f_J, fb, eq_S):
                f_J.append(fb)
                
        fI_fJ_generators = []
        for x in f_I:
            for y in f_J:
                fI_fJ_generators.append(mul_S(x, y))
        fI_fJ = ideal_generated_by(fI_fJ_generators, S, add_S, mul_S, zero_S, eq_S)
        
        subset1 = all(contains(fI_fJ, x, eq_S) for x in f_IJ)
        subset2 = all(contains(f_IJ, x, eq_S) for x in fI_fJ)
        
        neg_q = not (subset1 and subset2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "¬Q: f(IJ) != f(I)f(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3