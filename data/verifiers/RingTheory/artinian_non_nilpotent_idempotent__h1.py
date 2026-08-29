import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def mod_n(x, n):
    if n == 0:
        return x
    if hasattr(x, 'applyfunc'):
        return x.applyfunc(lambda a: a % n)
    else:
        return x % n

def eq(a, b, n):
    if n == 0:
        return a == b
    if hasattr(a, 'applyfunc') and hasattr(b, 'applyfunc'):
        return a.applyfunc(lambda x: x % n) == b.applyfunc(lambda x: x % n)
    else:
        return (a - b) % n == 0

def contains(lst, elem, n):
    return any(eq(x, elem, n) for x in lst)

def additive_span(generators, n, max_size):
    span = []
    for g in generators:
        if not contains(span, g, n):
            span.append(g)
            if len(span) > max_size:
                return span
    
    i = 0
    while i < len(span):
        for g in generators:
            new_elem = mod_n(span[i] + g, n)
            if not contains(span, new_elem, n):
                span.append(new_elem)
                if len(span) > max_size:
                    return span
        i += 1
    return span

def conditions(witness):
    # Duck-typing for custom witness objects (e.g., infinite rings)
    if hasattr(witness, 'is_right_ideal'):
        try:
            h1 = bool(witness.is_right_ideal())
            h2 = not bool(witness.is_nilpotent())
            neg_q = not bool(witness.has_nonzero_idempotent())
            return [h1, h2, neg_q]
        except Exception:
            pass

    # SymPy PolyRing and Ideal duck-typing
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_sym, I_sym = witness
            if hasattr(R_sym, 'ideal') and hasattr(I_sym, 'ring'):
                if I_sym.ring == R_sym:
                    h1 = True
                    # In a polynomial ring over an integral domain, an ideal is nilpotent iff it is the zero ideal
                    h2 = not (I_sym == R_sym.ideal(0))
                    # In an integral domain, the only idempotents are 0 and 1
                    neg_q = not (I_sym == R_sym.ideal(1))
                    return [h1, h2, neg_q]
    except Exception:
        pass

    # Finite ring logic
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, n = witness
            elif len(witness) == 2:
                R, I = witness
                n = 0
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        zero = mod_n(R[0] - R[0], n)
        
        h1_ok = True
        if not I:
            h1_ok = False
        else:
            for i in I:
                if not contains(R, i, n):
                    h1_ok = False
                    break
            for i in I:
                for j in I:
                    if not contains(I, mod_n(i - j, n), n):
                        h1_ok = False
                        break
            for i in I:
                for r in R:
                    if not contains(I, mod_n(i * r, n), n):
                        h1_ok = False
                        break
                        
        if not h1_ok:
            h2_ok = False
        else:
            current_power = list(I)
            h2_ok = True
            for _ in range(len(R) + 1):
                if all(eq(x, zero, n) for x in current_power):
                    h2_ok = False
                    break
                prods = []
                for a in current_power:
                    for b in I:
                        prods.append(mod_n(a * b, n))
                current_power = additive_span(prods, n, len(R))
                
        has_nonzero_idempotent = False
        for i in I:
            if not eq(i, zero, n):
                if eq(mod_n(i * i, n), i, n):
                    has_nonzero_idempotent = True
                    break
        neg_q = not has_nonzero_idempotent
        
        return [h1_ok, h2_ok, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a right ideal of R",
    "H_2: I is not a nilpotent ideal",
    "¬Q: I does not contain a non-zero idempotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2