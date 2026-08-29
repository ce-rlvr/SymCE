import itertools
import functools
import math
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

# We provide a standard finite ring without identity as a potential witness component.
# Z8_even is the ring 2Z / 8Z = {0, 2, 4, 6} under addition and multiplication modulo 8.
Z8_even_elements = [0, 2, 4, 6]
def Z8_add(a, b): return (a + b) % 8
def Z8_mul(a, b): return (a * b) % 8
Z8_even = (Z8_even_elements, [0, 4], Z8_add, Z8_mul, 0)

def extract_witness(witness):
    R, I, add, mul, zero = None, None, None, None, None
    if isinstance(witness, tuple):
        if len(witness) >= 5:
            R, I, add, mul, zero = witness[0], witness[1], witness[2], witness[3], witness[4]
        elif len(witness) == 4:
            R, I, add, mul = witness[0], witness[1], witness[2], witness[3]
    elif hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        R, I, add, mul = witness.R, witness.I, witness.add, witness.mul
        zero = getattr(witness, 'zero', None)
    elif isinstance(witness, dict):
        R, I, add, mul = witness['R'], witness['I'], witness['add'], witness['mul']
        zero = witness.get('zero', None)
    else:
        raise ValueError("Cannot extract witness format.")
        
    if zero is None and R:
        for z in R:
            is_zero = True
            for a in R:
                try:
                    if add(a, z) != a:
                        is_zero = False
                        break
                except Exception:
                    is_zero = False
                    break
            if is_zero:
                zero = z
                break
                
    return R, I, add, mul, zero

def check_ring(R, add, mul, zero):
    try:
        if len(R) > 50:
            return False
    except TypeError:
        return False
    if zero not in R: return False
    for a in R:
        for b in R:
            if add(a, b) not in R: return False
            if mul(a, b) not in R: return False
    for a in R:
        if add(a, zero) != a or add(zero, a) != a: return False
        has_inv = False
        for b in R:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        for b in R:
            if add(a, b) != add(b, a): return False
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
    for a in R:
        for b in R:
            for c in R:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
    for a in R:
        for b in R:
            for c in R:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def check_ideal(R, I, add, mul, zero):
    if not I: return False
    for i in I:
        if i not in R: return False
    if zero not in I: return False
    for a in I:
        for b in I:
            if add(a, b) not in I: return False
        has_inv = False
        for b in I:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
    for r in R:
        for i in I:
            if mul(r, i) not in I: return False
            if mul(i, r) not in I: return False
    return True

def check_neg_q(R, I, add, mul, zero):
    generators = []
    for r in R:
        for i in I:
            g1 = mul(r, i)
            if g1 not in generators:
                generators.append(g1)
            g2 = mul(i, r)
            if g2 not in generators:
                generators.append(g2)
            
    closure = [zero]
    queue = [zero]
    while queue:
        curr = queue.pop(0)
        for g in generators:
            nxt = add(curr, g)
            if nxt not in closure:
                closure.append(nxt)
                queue.append(nxt)
                
    for i in I:
        if i not in closure:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        R, I, add, mul, zero = extract_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = check_ring(R, add, mul, zero) and check_ideal(R, I, add, mul, zero)
    except Exception:
        h1_ok = False
        
    h2_ok = h1_ok
    
    try:
        neg_q_ok = check_neg_q(R, I, add, mul, zero)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: pi is the natural ring homomorphism",
    "not Q: The kernel of pi is not the ideal generated by I"
]

N_HYP = 2
NEG_Q_INDEX = 2