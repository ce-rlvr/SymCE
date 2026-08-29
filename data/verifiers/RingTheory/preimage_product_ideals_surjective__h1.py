import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def extract_ring(ring_obj):
    if isinstance(ring_obj, dict):
        elems = ring_obj['elements']
        add = ring_obj['add']
        mul = ring_obj['mul']
        zero = ring_obj.get('zero')
    else:
        elems = ring_obj.elements
        add = ring_obj.add
        mul = ring_obj.mul
        zero = getattr(ring_obj, 'zero', None)
    
    elems = list(elems)
    if zero is None:
        for z in elems:
            if all(add(z, a) == a and add(a, z) == a for a in elems):
                zero = z
                break
    return elems, add, mul, zero

def generate_ideal(elems, add, mul, zero, generators):
    ideal = set(generators)
    if not ideal and zero is not None:
        ideal.add(zero)
    changed = True
    while changed:
        changed = False
        new_elems = set()
        for x in ideal:
            for y in ideal:
                s = add(x, y)
                if s not in ideal and s not in new_elems:
                    new_elems.add(s)
            for r in elems:
                rx = mul(r, x)
                if rx not in ideal and rx not in new_elems:
                    new_elems.add(rx)
                xr = mul(x, r)
                if xr not in ideal and xr not in new_elems:
                    new_elems.add(xr)
        # Additive inverses
        for x in ideal:
            for y in elems:
                if add(x, y) == zero and add(y, x) == zero:
                    if y not in ideal and y not in new_elems:
                        new_elems.add(y)
        if new_elems:
            ideal.update(new_elems)
            changed = True
    return ideal

def is_ideal(elems, add, mul, zero, subset):
    if zero is None or zero not in subset:
        return False
    for x in subset:
        for y in subset:
            if add(x, y) not in subset:
                return False
        inv_found = False
        for y in subset:
            if add(x, y) == zero and add(y, x) == zero:
                if y in subset:
                    inv_found = True
                    break
        if not inv_found:
            return False
        for r in elems:
            if mul(r, x) not in subset:
                return False
            if mul(x, r) not in subset:
                return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            f = witness['f']
            I = witness['I']
            J = witness['J']
        else:
            R = witness.R
            S = witness.S
            f = witness.f
            I = witness.I
            J = witness.J
            
        R_elems, add_R, mul_R, zero_R = extract_ring(R)
        S_elems, add_S, mul_S, zero_S = extract_ring(S)
        
        if isinstance(f, dict):
            f_call = lambda x: f[x]
        else:
            f_call = f
            
        I = set(I)
        J = set(J)
    except Exception:
        return [False, False, False]
        
    # H1: f is a surjective ring homomorphism
    h1 = True
    try:
        mapped = set()
        for r in R_elems:
            fr = f_call(r)
            mapped.add(fr)
            if fr not in S_elems:
                h1 = False
        if not all(s in mapped for s in S_elems):
            h1 = False
        for a in R_elems:
            for b in R_elems:
                if f_call(add_R(a, b)) != add_S(f_call(a), f_call(b)):
                    h1 = False
                if f_call(mul_R(a, b)) != mul_S(f_call(a), f_call(b)):
                    h1 = False
    except Exception:
        h1 = False
        
    # H2: I and J are ideals of S
    h2 = True
    try:
        if not is_ideal(S_elems, add_S, mul_S, zero_S, I):
            h2 = False
        if not is_ideal(S_elems, add_S, mul_S, zero_S, J):
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: f^{-1}(IJ) != f^{-1}(I)f^{-1}(J) + ker(f)
    neg_q = False
    try:
        # Compute IJ
        IJ_gens = {mul_S(a, b) for a in I for b in J}
        IJ = generate_ideal(S_elems, add_S, mul_S, zero_S, IJ_gens)
        
        # Compute f^{-1}(IJ)
        f_inv_IJ = {r for r in R_elems if f_call(r) in IJ}
        
        # Compute f^{-1}(I) and f^{-1}(J)
        f_inv_I = {r for r in R_elems if f_call(r) in I}
        f_inv_J = {r for r in R_elems if f_call(r) in J}
        
        # Compute f^{-1}(I)f^{-1}(J)
        prod_gens = {mul_R(u, v) for u in f_inv_I for v in f_inv_J}
        f_inv_I_f_inv_J = generate_ideal(R_elems, add_R, mul_R, zero_R, prod_gens)
        
        # Compute ker(f)
        ker_f = {r for r in R_elems if f_call(r) == zero_S}
        
        # Compute sum
        ideal_sum = {add_R(a, b) for a in f_inv_I_f_inv_J for b in ker_f}
        
        if f_inv_IJ != ideal_sum:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: I and J are ideals of S",
    "¬Q: The preimage f^{-1}(IJ) is not equal to the ideal sum f^{-1}(I)f^{-1}(J) + ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2