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

def get_ring_props(witness, name):
    try:
        if isinstance(witness, dict):
            ring_obj = witness.get(name)
            if isinstance(ring_obj, dict) and 'elements' in ring_obj:
                return (
                    list(ring_obj['elements']),
                    ring_obj['add'],
                    ring_obj['mul'],
                    ring_obj['zero'],
                    ring_obj['one']
                )
            else:
                return (
                    list(witness[name]),
                    witness[f'add_{name}'],
                    witness[f'mul_{name}'],
                    witness[f'zero_{name}'],
                    witness[f'one_{name}']
                )
        else:
            ring_obj = getattr(witness, name)
            if hasattr(ring_obj, 'elements'):
                return (
                    list(ring_obj.elements),
                    ring_obj.add,
                    ring_obj.mul,
                    ring_obj.zero,
                    ring_obj.one
                )
            else:
                return (
                    list(getattr(witness, name)),
                    getattr(witness, f'add_{name}'),
                    getattr(witness, f'mul_{name}'),
                    getattr(witness, f'zero_{name}'),
                    getattr(witness, f'one_{name}')
                )
    except Exception:
        return None, None, None, None, None

def get_ideal(witness, name):
    try:
        if isinstance(witness, dict):
            ideal = witness.get(name)
        else:
            ideal = getattr(witness, name)
            
        if hasattr(ideal, 'elements'):
            return list(ideal.elements)
        return list(ideal)
    except Exception:
        return None

def get_f(witness):
    try:
        if isinstance(witness, dict):
            f_val = witness.get('f')
        else:
            f_val = getattr(witness, 'f')
            
        if isinstance(f_val, dict):
            return lambda x: f_val[x]
        if isinstance(f_val, list):
            f_dict = dict(f_val)
            return lambda x: f_dict[x]
        return f_val
    except Exception:
        return None

def is_finite_ring(elements, add, mul, zero, one):
    try:
        if not isinstance(elements, (list, tuple, set)):
            return False
        elements = list(elements)
        if zero not in elements or one not in elements:
            return False
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True
    except Exception:
        return False

def is_ideal(elements, add, mul, zero, ideal_elements):
    try:
        if not isinstance(ideal_elements, (list, tuple, set)): return False
        ideal_elements = list(ideal_elements)
        if not ideal_elements: return False
        if zero not in ideal_elements: return False
        for a in ideal_elements:
            if a not in elements: return False
            for b in ideal_elements:
                if add(a, b) not in ideal_elements: return False
            for r in elements:
                if mul(r, a) not in ideal_elements: return False
                if mul(a, r) not in ideal_elements: return False
        return True
    except Exception:
        return False

def are_comaximal(elements, add, I_elements, J_elements):
    try:
        sums = []
        for i in I_elements:
            for j in J_elements:
                s = add(i, j)
                if s not in sums:
                    sums.append(s)
        for e in elements:
            if e not in sums:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple) and len(witness) == 5:
        witness = {
            'R': witness[0],
            'S': witness[1],
            'I': witness[2],
            'J': witness[3],
            'f': witness[4]
        }

    R_elements, add_R, mul_R, zero_R, one_R = get_ring_props(witness, 'R')
    S_elements, add_S, mul_S, zero_S, one_S = get_ring_props(witness, 'S')
    I_elements = get_ideal(witness, 'I')
    J_elements = get_ideal(witness, 'J')
    f = get_f(witness)

    if any(x is None for x in [R_elements, add_R, mul_R, zero_R, one_R,
                               S_elements, add_S, mul_S, zero_S, one_S,
                               I_elements, J_elements, f]):
        return [False, False, False]

    # H1: R and S are rings
    try:
        h1 = is_finite_ring(R_elements, add_R, mul_R, zero_R, one_R) and \
             is_finite_ring(S_elements, add_S, mul_S, zero_S, one_S)
    except Exception:
        h1 = False

    # H2: I and J are comaximal ideals in S
    try:
        h2 = is_ideal(S_elements, add_S, mul_S, zero_S, I_elements) and \
             is_ideal(S_elements, add_S, mul_S, zero_S, J_elements) and \
             are_comaximal(S_elements, add_S, I_elements, J_elements)
    except Exception:
        h2 = False

    # neg_Q: f is a ring hom, and preimages are not comaximal
    try:
        is_hom = True
        if f(one_R) != one_S:
            is_hom = False
        for a in R_elements:
            if f(a) not in S_elements:
                is_hom = False
                break
            for b in R_elements:
                if f(add_R(a, b)) != add_S(f(a), f(b)):
                    is_hom = False
                    break
                if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                    is_hom = False
                    break
            if not is_hom:
                break
        
        if not is_hom:
            neg_q = False
        else:
            pre_I = [x for x in R_elements if f(x) in I_elements]
            pre_J = [x for x in R_elements if f(x) in J_elements]
            
            sums = []
            for i in pre_I:
                for j in pre_J:
                    s = add_R(i, j)
                    if s not in sums:
                        sums.append(s)
                    
            neg_q = False
            for e in R_elements:
                if e not in sums:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: I and J are comaximal ideals in S",
    "¬Q: The preimage ideals f^{-1}(I) and f^{-1}(J) are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2