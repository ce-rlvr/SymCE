import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def make_callable(op):
    if isinstance(op, dict):
        return lambda a, b: op[(a, b)]
    return op

def get_ring_data(witness, name):
    try:
        ring = getattr(witness, name)
        return list(ring.elements), make_callable(ring.add), make_callable(ring.mul), ring.zero
    except Exception:
        pass
    try:
        ring = witness[name]
        return list(ring['elements']), make_callable(ring['add']), make_callable(ring['mul']), ring['zero']
    except Exception:
        pass
    try:
        return (list(getattr(witness, f"{name}_elements")),
                make_callable(getattr(witness, f"{name}_add")),
                make_callable(getattr(witness, f"{name}_mul")),
                getattr(witness, f"{name}_zero"))
    except Exception:
        pass
    try:
        return (list(witness[f"{name}_elements"]),
                make_callable(witness[f"{name}_add"]),
                make_callable(witness[f"{name}_mul"]),
                witness[f"{name}_zero"])
    except Exception:
        pass
    raise ValueError(f"Could not extract {name}")

def get_f(witness):
    try:
        f_obj = getattr(witness, 'f')
    except Exception:
        try:
            f_obj = witness['f']
        except Exception:
            raise ValueError("Could not extract f")
    
    if isinstance(f_obj, dict):
        return lambda x: f_obj[x]
    return f_obj

def is_commutative_ring(elements, add, mul, zero):
    if zero not in elements: return False
    
    # Check closure and commutativity
    for a in elements:
        for b in elements:
            try:
                s1 = add(a, b)
                s2 = add(b, a)
                p1 = mul(a, b)
                p2 = mul(b, a)
            except Exception:
                return False
            if s1 not in elements or p1 not in elements: return False
            if s1 != s2: return False
            if p1 != p2: return False
            
    # Check associativity and distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False

    # Check identity for addition (zero)
    for a in elements:
        if add(a, zero) != a: return False

    # Check additive inverses
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False

    return True

def is_homomorphism(elements_R, add_R, mul_R, zero_R, f, elements_S, add_S, mul_S, zero_S):
    # Check if f maps R to S
    for a in elements_R:
        try:
            fa = f(a)
        except Exception:
            return False
        if fa not in elements_S:
            return False

    # Check addition and multiplication preservation
    for a in elements_R:
        for b in elements_R:
            if f(add_R(a, b)) != add_S(f(a), f(b)): return False
            if f(mul_R(a, b)) != mul_S(f(a), f(b)): return False
            
    return True

def get_nilradical(elements, mul, zero):
    nil_elements = []
    for x in elements:
        curr = x
        is_nil = False
        for _ in range(len(elements)):
            if curr == zero:
                is_nil = True
                break
            curr = mul(curr, x)
        if is_nil:
            nil_elements.append(x)
    return nil_elements

def conditions(witness) -> list[bool]:
    try:
        R_elements, R_add, R_mul, R_zero = get_ring_data(witness, 'R')
        S_elements, S_add, S_mul, S_zero = get_ring_data(witness, 'S')
        f = get_f(witness)
    except Exception:
        return [False, False, False]

    # H_1: R and S are commutative rings
    try:
        h1 = is_commutative_ring(R_elements, R_add, R_mul, R_zero) and \
             is_commutative_ring(S_elements, S_add, S_mul, S_zero)
    except Exception:
        h1 = False

    # H_2: f: R \to S is a ring homomorphism
    try:
        h2 = is_homomorphism(R_elements, R_add, R_mul, R_zero, f, S_elements, S_add, S_mul, S_zero)
    except Exception:
        h2 = False

    # ¬Q: f(Nil(R)) \not\subseteq Nil(S)
    try:
        R_nil = get_nilradical(R_elements, R_mul, R_zero)
        S_nil = get_nilradical(S_elements, S_mul, S_zero)
        
        neg_q = False
        for x in R_nil:
            if f(x) not in S_nil:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R \\to S is a ring homomorphism",
    "¬Q: f(\\text{Nil}(R)) \\not\\subseteq \\text{Nil}(S)"
]

N_HYP = 2
NEG_Q_INDEX = 2