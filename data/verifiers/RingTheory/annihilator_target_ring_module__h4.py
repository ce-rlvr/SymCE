import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: f maps the multiplicative identity of R to the multiplicative identity of S",
    "¬Q: The annihilator of S as an R-module is not exactly the kernel of f"
]

N_HYP = 3
NEG_Q_INDEX = 3

def eq(a, b):
    if a == b: return True
    try:
        if a - b == 0: return True
    except Exception:
        pass
    try:
        if sympy.simplify(a - b) == 0: return True
    except Exception:
        pass
    return False

def get_elements(ring):
    if hasattr(ring, 'elements'):
        return list(ring.elements)
    elif hasattr(ring, 'elements_list'):
        return ring.elements_list()
    elif hasattr(ring, '__iter__'):
        return list(ring)
    else:
        raise ValueError("Cannot get elements")

def get_zero(ring):
    if hasattr(ring, 'zero'): return ring.zero
    return 0

def get_one(ring):
    if hasattr(ring, 'one'): return ring.one
    return 1

def add(ring, a, b):
    if hasattr(ring, 'add'): return ring.add(a, b)
    return a + b

def mul(ring, a, b):
    if hasattr(ring, 'mul'): return ring.mul(a, b)
    return a * b

def apply_f(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def apply_action(action, r, s):
    if isinstance(action, dict):
        return action[(r, s)]
    return action(r, s)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            f = witness['f']
            action = witness.get('action', None)
        else:
            try:
                R = witness.R
                S = witness.S
                f = witness.f
            except AttributeError:
                R, S, f = witness
            
            if hasattr(witness, 'action'):
                action = witness.action
            elif hasattr(witness, 'rmul'):
                action = witness.rmul
            else:
                action = None
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings with identity
    try:
        if hasattr(R, 'is_ring_with_identity') and hasattr(S, 'is_ring_with_identity'):
            h1 = bool(R.is_ring_with_identity() and S.is_ring_with_identity())
        else:
            z_R = get_zero(R)
            o_R = get_one(R)
            elems_R = get_elements(R)
            h1_R = True
            for x in elems_R:
                if not eq(add(R, x, z_R), x) or not eq(add(R, z_R, x), x): h1_R = False
                if not eq(mul(R, x, o_R), x) or not eq(mul(R, o_R, x), x): h1_R = False
                
            z_S = get_zero(S)
            o_S = get_one(S)
            elems_S = get_elements(S)
            h1_S = True
            for x in elems_S:
                if not eq(add(S, x, z_S), x) or not eq(add(S, z_S, x), x): h1_S = False
                if not eq(mul(S, x, o_S), x) or not eq(mul(S, o_S, x), x): h1_S = False
                
            h1 = bool(h1_R and h1_S)
    except Exception:
        h1 = False

    # H_2: f is a ring homomorphism from R to S
    try:
        if hasattr(f, 'is_ring_homomorphism'):
            h2 = bool(f.is_ring_homomorphism(R, S))
        else:
            h2 = True
            elems_R = get_elements(R)
            for x in elems_R:
                for y in elems_R:
                    if not eq(apply_f(f, add(R, x, y)), add(S, apply_f(f, x), apply_f(f, y))): h2 = False
                    if not eq(apply_f(f, mul(R, x, y)), mul(S, apply_f(f, x), apply_f(f, y))): h2 = False
    except Exception:
        h2 = False

    # H_3: f maps the multiplicative identity of R to the multiplicative identity of S
    try:
        h3 = bool(eq(apply_f(f, get_one(R)), get_one(S)))
    except Exception:
        h3 = False

    # ¬Q: The annihilator of S as an R-module is not exactly the kernel of f
    try:
        elems_R = get_elements(R)
        elems_S = get_elements(S)
        z_S = get_zero(S)
        
        ker_f = []
        for r in elems_R:
            if eq(apply_f(f, r), z_S):
                ker_f.append(r)
                
        ann_S = []
        for r in elems_R:
            is_ann = True
            for s in elems_S:
                if action is not None:
                    val = apply_action(action, r, s)
                else:
                    val = mul(S, apply_f(f, r), s)
                if not eq(val, z_S):
                    is_ann = False
                    break
            if is_ann:
                ann_S.append(r)
                
        ker_f_subset_ann_S = all(any(eq(x, y) for y in ann_S) for x in ker_f)
        ann_S_subset_ker_f = all(any(eq(x, y) for y in ker_f) for x in ann_S)
        
        neg_q = not (ker_f_subset_ann_S and ann_S_subset_ker_f)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]