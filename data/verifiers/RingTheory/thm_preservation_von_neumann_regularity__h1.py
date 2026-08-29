import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness expressions
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

def apply2(op, a, b):
    if isinstance(op, dict):
        return op[(a, b)]
    elif isinstance(op, (list, tuple)):
        return op[a][b]
    return op(a, b)

def apply1(op, a):
    if isinstance(op, dict):
        return op[a]
    elif isinstance(op, (list, tuple)):
        return op[a]
    return op(a)

def is_ring(elements, add, mul):
    elements = list(elements)
    # closure
    for a in elements:
        for b in elements:
            try:
                if apply2(add, a, b) not in elements: return False
                if apply2(mul, a, b) not in elements: return False
            except Exception:
                return False
            
    # associativity and distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                try:
                    if apply2(add, apply2(add, a, b), c) != apply2(add, a, apply2(add, b, c)): return False
                    if apply2(mul, apply2(mul, a, b), c) != apply2(mul, a, apply2(mul, b, c)): return False
                    if apply2(mul, a, apply2(add, b, c)) != apply2(add, apply2(mul, a, b), apply2(mul, a, c)): return False
                    if apply2(mul, apply2(add, a, b), c) != apply2(add, apply2(mul, a, c), apply2(mul, b, c)): return False
                except Exception:
                    return False

    # commutativity of add
    for a in elements:
        for b in elements:
            try:
                if apply2(add, a, b) != apply2(add, b, a): return False
            except Exception:
                return False

    # zero
    zeros_list = []
    for z in elements:
        try:
            if all(apply2(add, z, a) == a for a in elements):
                zeros_list.append(z)
        except Exception:
            return False
    if len(zeros_list) != 1: return False
    z = zeros_list[0]

    # inverses
    for a in elements:
        try:
            if not any(apply2(add, a, b) == z for b in elements): return False
        except Exception:
            return False

    return True

def is_vn_regular(elements, mul):
    elements = list(elements)
    for a in elements:
        has_x = False
        for x in elements:
            try:
                axa = apply2(mul, apply2(mul, a, x), a)
                if axa == a:
                    has_x = True
                    break
            except Exception:
                pass
        if not has_x:
            return False
    return True

def extract_ring(obj):
    if isinstance(obj, dict):
        return list(obj['elements']), obj['add'], obj['mul']
    elif isinstance(obj, (list, tuple)) and len(obj) == 3:
        return list(obj[0]), obj[1], obj[2]
    else:
        return list(obj.elements), obj.add, obj.mul

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict) and 'R_elements' in witness:
            R_elements = list(witness['R_elements'])
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_elements = list(witness['S_elements'])
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            f = witness['f']
        elif isinstance(witness, dict) and 'R' in witness:
            R_elements, R_add, R_mul = extract_ring(witness['R'])
            S_elements, S_add, S_mul = extract_ring(witness['S'])
            f = witness['f']
        elif isinstance(witness, tuple) and len(witness) == 3:
            R_elements, R_add, R_mul = extract_ring(witness[0])
            S_elements, S_add, S_mul = extract_ring(witness[1])
            f = witness[2]
        else:
            R_elements, R_add, R_mul = extract_ring(witness.R)
            S_elements, S_add, S_mul = extract_ring(witness.S)
            f = witness.f
    except Exception:
        return [False, False, False]

    # H1: f is a surjective ring homomorphism from R to S
    h1 = False
    try:
        if is_ring(R_elements, R_add, R_mul) and is_ring(S_elements, S_add, S_mul):
            maps_to_S = True
            for r in R_elements:
                if apply1(f, r) not in S_elements:
                    maps_to_S = False
                    break
            
            if maps_to_S:
                surjective = True
                for s in S_elements:
                    if not any(apply1(f, r) == s for r in R_elements):
                        surjective = False
                        break
                
                if surjective:
                    homo = True
                    for a in R_elements:
                        for b in R_elements:
                            f_a = apply1(f, a)
                            f_b = apply1(f, b)
                            if apply1(f, apply2(R_add, a, b)) != apply2(S_add, f_a, f_b):
                                homo = False
                                break
                            if apply1(f, apply2(R_mul, a, b)) != apply2(S_mul, f_a, f_b):
                                homo = False
                                break
                        if not homo:
                            break
                    if homo:
                        h1 = True
    except Exception:
        h1 = False

    # H2: R is a von Neumann regular ring
    h2 = False
    try:
        h2 = is_vn_regular(R_elements, R_mul)
    except Exception:
        h2 = False

    # Conclusion: S is a von Neumann regular ring (negated for counterexample)
    neg_q = False
    try:
        q = is_vn_regular(S_elements, S_mul)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: R is a von Neumann regular ring",
    "¬Q: S is not a von Neumann regular ring"
]

N_HYP = 2
NEG_Q_INDEX = 2