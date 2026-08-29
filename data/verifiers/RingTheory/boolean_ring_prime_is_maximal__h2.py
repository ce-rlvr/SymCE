import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(obj, name):
    if hasattr(obj, name):
        return getattr(obj, name)
    elif isinstance(obj, dict) and name in obj:
        return obj[name]
    raise AttributeError(name)

def get_witness_attrs(witness):
    try:
        elements = get_attr(witness, 'elements')
    except AttributeError:
        elements = get_attr(witness, 'R')
    elements = list(elements)
    add = get_attr(witness, 'add')
    mul = get_attr(witness, 'mul')
    zero = get_attr(witness, 'zero')
    P = list(get_attr(witness, 'P'))
    return elements, add, mul, zero, P

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero, P = get_witness_attrs(witness)
    except Exception:
        return [False, False, False]
        
    # H1: R is a Boolean ring
    try:
        h1 = True
        if zero not in elements: 
            h1 = False
        else:
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a: h1 = False
                if mul(a, a) != a: h1 = False
            for a in elements:
                for b in elements:
                    if add(a, b) != add(b, a): h1 = False
                    if mul(a, b) != mul(b, a): h1 = False
            for a in elements:
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv: h1 = False
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): h1 = False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): h1 = False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): h1 = False
    except Exception:
        h1 = False

    # H2: P is a prime ideal of R
    try:
        h2 = True
        for p in P:
            if p not in elements: h2 = False
        if zero not in P: h2 = False
        for a in P:
            for b in P:
                if add(a, b) not in P: h2 = False
        for a in P:
            inv_found = False
            for b in P:
                if add(a, b) == zero:
                    inv_found = True
                    break
            if not inv_found: h2 = False
        for r in elements:
            for p in P:
                if mul(r, p) not in P: h2 = False
                if mul(p, r) not in P: h2 = False
        for a in elements:
            for b in elements:
                if mul(a, b) in P:
                    if a not in P and b not in P:
                        h2 = False
    except Exception:
        h2 = False

    # neg_Q: P is NOT a maximal ideal of R
    try:
        is_maximal = True
        is_proper = False
        for e in elements:
            if e not in P:
                is_proper = True
                break
        
        if not is_proper:
            is_maximal = False
        else:
            for x in elements:
                if x in P: continue
                I = list(P)
                if x not in I: I.append(x)
                changed = True
                while changed:
                    changed = False
                    new_I = list(I)
                    for a in I:
                        for b in I:
                            s = add(a, b)
                            if s not in new_I:
                                new_I.append(s)
                                changed = True
                    for a in I:
                        for r in elements:
                            m1 = mul(a, r)
                            if m1 not in new_I:
                                new_I.append(m1)
                                changed = True
                            m2 = mul(r, a)
                            if m2 not in new_I:
                                new_I.append(m2)
                                changed = True
                    I = new_I
                
                I_is_proper = False
                for e in elements:
                    if e not in I:
                        I_is_proper = True
                        break
                if I_is_proper:
                    is_maximal = False
                    break
                    
        neg_q = not is_maximal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2