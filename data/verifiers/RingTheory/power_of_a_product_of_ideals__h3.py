import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def extract_RIJn(witness):
    if isinstance(witness, tuple) and len(witness) == 4:
        return witness
    if isinstance(witness, dict) and all(k in witness for k in ('R', 'I', 'J', 'n')):
        return witness['R'], witness['I'], witness['J'], witness['n']
    return None

def check_commutative_ring(R):
    if not R: return False
    zero = None
    for r in R:
        if all(bool(x + r == x) and bool(r + x == x) for x in R):
            zero = r
            break
    if zero is None: return False
    
    for a in R:
        if not any(bool(a + b == zero) and bool(b + a == zero) for b in R):
            return False
            
    for a in R:
        for b in R:
            try:
                sm = a + b
                pr = a * b
            except Exception:
                return False
            
            if not any(bool(sm == x) for x in R): return False
            if not bool(sm == b + a): return False
            
            if not any(bool(pr == x) for x in R): return False
            if not bool(pr == b * a): return False
            
    for a in R:
        for b in R:
            for c in R:
                if not bool((a + b) + c == a + (b + c)): return False
                if not bool((a * b) * c == a * (b * c)): return False
                if not bool(a * (b + c) == a * b + a * c): return False
                
    return True

def check_ideals(R, I, J):
    for x in I:
        if not any(bool(x == r) for r in R): return False
    for x in J:
        if not any(bool(x == r) for r in R): return False
        
    for a in I:
        for b in I:
            sm = a + b
            if not any(bool(sm == x) for x in I): return False
        for r in R:
            pr1 = a * r
            pr2 = r * a
            if not any(bool(pr1 == x) for x in I): return False
            if not any(bool(pr2 == x) for x in I): return False
            
    for a in J:
        for b in J:
            sm = a + b
            if not any(bool(sm == x) for x in J): return False
        for r in R:
            pr1 = a * r
            pr2 = r * a
            if not any(bool(pr1 == x) for x in J): return False
            if not any(bool(pr2 == x) for x in J): return False
            
    return True

def ideal_closure(S, R):
    ideal = []
    for s in S:
        if not any(bool(s == x) for x in ideal):
            ideal.append(s)
            
    for s in S:
        for r in R:
            p1 = s * r
            if not any(bool(p1 == x) for x in ideal): ideal.append(p1)
            p2 = r * s
            if not any(bool(p2 == x) for x in ideal): ideal.append(p2)
            
    changed = True
    while changed:
        changed = False
        n_ideal = len(ideal)
        for i in range(n_ideal):
            for j in range(i, n_ideal):
                sm = ideal[i] + ideal[j]
                if not any(bool(sm == x) for x in ideal):
                    ideal.append(sm)
                    changed = True
    return ideal

def product_ideal(I, J, R):
    gens = []
    for i in I:
        for j in J:
            gens.append(i * j)
    return ideal_closure(gens, R)

def power_ideal(I, n, R):
    if n < 0 or n > 10:
        return None
    if n == 0:
        one = None
        for r in R:
            if all(bool(r * x == x) and bool(x * r == x) for x in R):
                one = r
                break
        if one is None: return None
        return ideal_closure([one], R)
    res = I
    for _ in range(n - 1):
        res = product_ideal(res, I, R)
    return res

def conditions(witness) -> list[bool]:
    # H1: R is a commutative ring
    h1 = False
    try:
        if hasattr(witness, 'is_commutative_ring'):
            h1 = bool(witness.is_commutative_ring())
        else:
            extracted = extract_RIJn(witness)
            if extracted:
                R, I, J, n = extracted
                if isinstance(R, (list, tuple)):
                    h1 = check_commutative_ring(R)
    except Exception:
        h1 = False

    # H2: I and J are ideals of R
    h2 = False
    try:
        if hasattr(witness, 'are_ideals'):
            h2 = bool(witness.are_ideals())
        else:
            extracted = extract_RIJn(witness)
            if extracted:
                R, I, J, n = extracted
                if isinstance(R, (list, tuple)):
                    h2 = check_ideals(R, I, J)
    except Exception:
        h2 = False

    # neg_Q: (IJ)^n != I^n J^n
    neg_q = False
    try:
        if hasattr(witness, 'conclusion_fails'):
            neg_q = bool(witness.conclusion_fails())
        else:
            extracted = extract_RIJn(witness)
            if extracted:
                R, I, J, n = extracted
                if isinstance(R, (list, tuple)):
                    IJ = product_ideal(I, J, R)
                    IJ_n = power_ideal(IJ, n, R)
                    I_n = power_ideal(I, n, R)
                    J_n = power_ideal(J, n, R)
                    if IJ_n is not None and I_n is not None and J_n is not None:
                        In_Jn = product_ideal(I_n, J_n, R)
                        def subset(A, B):
                            for a in A:
                                if not any(bool(a == b) for b in B): return False
                            return True
                        neg_q = not (subset(IJ_n, In_Jn) and subset(In_Jn, IJ_n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "¬Q: (IJ)^n != I^n J^n"
]

N_HYP = 2
NEG_Q_INDEX = 2