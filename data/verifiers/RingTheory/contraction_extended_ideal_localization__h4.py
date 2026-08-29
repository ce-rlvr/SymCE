import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Setup bindings
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

def extract_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            R, S, I = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            zero = None
        elif len(witness) == 6:
            R, S, I, add, mul, zero = witness
        else:
            raise ValueError("Invalid tuple length")
    else:
        R = witness.R
        S = witness.S
        I = witness.I
        add = witness.add if hasattr(witness, 'add') else lambda a, b: a + b
        mul = witness.mul if hasattr(witness, 'mul') else lambda a, b: a * b
        zero = witness.zero if hasattr(witness, 'zero') else None
        
    def get_unique(lst):
        res = []
        for x in lst:
            if x not in res:
                res.append(x)
        return res
        
    R = get_unique(list(R))
    S = get_unique(list(S))
    I = get_unique(list(I))
    
    if zero is None:
        for x in R:
            if all(add(x, y) == y for y in R):
                zero = x
                break
    if zero is None:
        raise ValueError("No zero found")
                
    return R, S, I, add, mul, zero

def check_H1(R, add, mul, zero):
    if zero not in R: return False
    for a in R:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
    for a in R:
        for b in R:
            if add(a, b) not in R: return False
            if add(a, b) != add(b, a): return False
            if mul(a, b) not in R: return False
            if mul(a, b) != mul(b, a): return False
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    for a in R:
        has_inv = False
        for b in R:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
    return True

def check_H2(R, S, mul):
    if not all(s in R for s in S): return False
    for a in S:
        for b in S:
            if mul(a, b) not in S: return False
    return True

def check_H3(R, I, add, mul, zero):
    if zero not in I: return False
    if not all(x in R for x in I): return False
    for a in I:
        for b in I:
            if add(a, b) not in I: return False
        has_inv = False
        for b in I:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
    for r in R:
        for a in I:
            if mul(r, a) not in I: return False
    return True

def check_neg_Q(R, S, I, add, mul, zero):
    RHS = []
    for x in R:
        for s in S:
            if mul(s, x) in I:
                RHS.append(x)
                break
                
    identity = None
    for x in R:
        if all(mul(x, y) == y and mul(y, x) == y for y in R):
            identity = x
            break
            
    # The canonical map phi(x) = x/1 requires 1 in S.
    # If 1 is not in S, the map is undefined, and the conclusion fails.
    if identity is None or identity not in S:
        return True
        
    neg_map = {}
    for y in R:
        for z in R:
            if add(y, z) == zero:
                neg_map[y] = z
                break

    LHS = []
    for x in R:
        in_LHS = False
        for a in I:
            neg_a = neg_map.get(a)
            if neg_a is None:
                return False
            for s in S:
                term1 = mul(x, s)
                diff = add(term1, neg_a)
                
                equiv = False
                for u in S:
                    if mul(u, diff) == zero:
                        equiv = True
                        break
                if equiv:
                    in_LHS = True
                    break
            if in_LHS:
                break
        if in_LHS:
            LHS.append(x)
            
    for x in R:
        if (x in LHS) != (x in RHS):
            return True
            
    return False

def conditions(witness):
    try:
        R, S, I, add, mul, zero = extract_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_H1(R, add, mul, zero)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(R, S, mul)
    except Exception:
        h2 = False
        
    try:
        h3 = check_H3(R, I, add, mul, zero)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(R, S, I, add, mul, zero)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: I is an ideal of R",
    r"¬Q: The contraction of the extended ideal \phi^{-1}(S^{-1}I) is not equal to \{x \in R \mid \exists s \in S \text{ such that } sx \in I\}"
]

N_HYP = 3
NEG_Q_INDEX = 3