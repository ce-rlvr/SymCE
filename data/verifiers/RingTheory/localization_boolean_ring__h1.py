import itertools

# Top-level setup for standard objects
# (No specific named objects required for this general ring theory verifier,
# but we provide standard bindings as requested)
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def extract(witness):
    if isinstance(witness, dict):
        return witness['elements'], witness['P'], witness['add'], witness['mul'], witness['zero']
    if isinstance(witness, tuple) and len(witness) == 5:
        return witness
    return witness.elements, witness.P, witness.add, witness.mul, witness.zero

def is_boolean_ring(elements, add, mul, zero):
    elements = list(elements)
    if zero not in elements:
        return False
    for x in elements:
        if mul(x, x) != x: return False
        if add(x, zero) != x: return False
        if add(zero, x) != x: return False
        if add(x, x) != zero: return False
    for x in elements:
        for y in elements:
            if add(x, y) != add(y, x): return False
            if mul(x, y) != mul(y, x): return False
            for z in elements:
                if add(x, add(y, z)) != add(add(x, y), z): return False
                if mul(x, mul(y, z)) != mul(mul(x, y), z): return False
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
    return True

def is_prime_ideal(elements, P, add, mul, zero):
    elements = list(elements)
    P = list(P)
    if zero not in P:
        return False
    for x in P:
        if x not in elements:
            return False
    for x in P:
        for y in P:
            if add(x, y) not in P: return False
    for x in P:
        for r in elements:
            if mul(x, r) not in P: return False
    for a in elements:
        for b in elements:
            if mul(a, b) in P:
                if a not in P and b not in P:
                    return False
    return True

def compute_R_P(elements, P, add, mul, zero):
    elements = list(elements)
    P = list(P)
    S = [x for x in elements if x not in P]
    if not S:
        return [] 
    
    classes = []
    for a in elements:
        for s in S:
            found = False
            for cls in classes:
                b, t = cls[0]
                equiv = False
                for u in S:
                    at = mul(a, t)
                    bs = mul(b, s)
                    diff = add(at, bs)
                    if mul(u, diff) == zero:
                        equiv = True
                        break
                if equiv:
                    cls.append((a, s))
                    found = True
                    break
            if not found:
                classes.append([(a, s)])
    return classes

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_boolean_ring'):
            h1 = witness.is_boolean_ring()
        else:
            elements, P, add, mul, zero = extract(witness)
            h1 = is_boolean_ring(elements, add, mul, zero)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_prime_ideal'):
            h2 = witness.is_prime_ideal()
        else:
            elements, P, add, mul, zero = extract(witness)
            h2 = is_prime_ideal(elements, P, add, mul, zero)
    except Exception:
        h2 = False

    try:
        if hasattr(witness, 'localization_is_Z2'):
            neg_q = not witness.localization_is_Z2()
        else:
            elements, P, add, mul, zero = extract(witness)
            classes = compute_R_P(elements, P, add, mul, zero)
            neg_q = (len(classes) != 2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: P is a prime ideal of R",
    "¬Q: The localization R_P is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2