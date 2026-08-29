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

def _get_attr(w, name):
    if isinstance(w, dict) and name in w:
        return w[name]
    if hasattr(w, name):
        attr = getattr(w, name)
        return attr() if callable(attr) and name in ['elements', 'zero', 'one'] else attr
    raise AttributeError(f"Missing {name}")

def conditions(witness):
    try:
        # Check H1: Euclidean ring
        if hasattr(witness, 'is_euclidean'):
            h1_val = getattr(witness, 'is_euclidean')
            if callable(h1_val): h1_val = h1_val()
            h1 = bool(h1_val)
        elif isinstance(witness, dict) and 'is_euclidean' in witness:
            h1_val = witness['is_euclidean']
            if callable(h1_val): h1_val = h1_val()
            h1 = bool(h1_val)
        else:
            elements = list(_get_attr(witness, 'elements'))
            add = _get_attr(witness, 'add')
            mul = _get_attr(witness, 'mul')
            zero = _get_attr(witness, 'zero')
            one = _get_attr(witness, 'one')
            f_raw = _get_attr(witness, 'f')
            if isinstance(f_raw, dict):
                f = lambda x: f_raw[x]
            else:
                f = f_raw
                
            is_ring = True
            
            if one == zero:
                is_ring = False
                
            if is_ring:
                for a in elements:
                    if add(a, zero) != a or add(zero, a) != a:
                        is_ring = False; break
                    if mul(a, one) != a or mul(one, a) != a:
                        is_ring = False; break
                    
                    has_inv = False
                    for b in elements:
                        if add(a, b) == zero and add(b, a) == zero:
                            has_inv = True; break
                    if not has_inv:
                        is_ring = False; break
                        
                    for b in elements:
                        if add(a, b) != add(b, a):
                            is_ring = False; break
                        if mul(a, b) != mul(b, a):
                            is_ring = False; break
                        for c in elements:
                            if add(add(a, b), c) != add(a, add(b, c)):
                                is_ring = False; break
                            if mul(mul(a, b), c) != mul(a, mul(b, c)):
                                is_ring = False; break
                            if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                                is_ring = False; break
                        if not is_ring: break
                    if not is_ring: break

            is_euclidean = False
            if is_ring:
                is_euclidean = True
                for a in elements:
                    if a != zero:
                        try:
                            val = f(a)
                            if not isinstance(val, int) or val < 0:
                                is_euclidean = False; break
                        except Exception:
                            is_euclidean = False; break
                
                if is_euclidean:
                    for a in elements:
                        for b in elements:
                            if b == zero: continue
                            found = False
                            for q in elements:
                                for r in elements:
                                    if a == add(mul(b, q), r):
                                        if r == zero or f(r) < f(b):
                                            found = True
                                            break
                                if found: break
                            if not found:
                                is_euclidean = False
                                break
                        if not is_euclidean: break
                        
            h1 = is_ring and is_euclidean
    except Exception:
        h1 = False
        
    try:
        # Check neg_Q: NOT a PID
        if hasattr(witness, 'is_pid'):
            pid_val = getattr(witness, 'is_pid')
            if callable(pid_val): pid_val = pid_val()
            neg_q = not bool(pid_val)
        elif isinstance(witness, dict) and 'is_pid' in witness:
            pid_val = witness['is_pid']
            if callable(pid_val): pid_val = pid_val()
            neg_q = not bool(pid_val)
        else:
            elements = list(_get_attr(witness, 'elements'))
            mul = _get_attr(witness, 'mul')
            zero = _get_attr(witness, 'zero')
            
            is_domain = True
            for a in elements:
                if a == zero: continue
                for b in elements:
                    if b == zero: continue
                    if mul(a, b) == zero:
                        is_domain = False
                        break
                if not is_domain: break
                
            # For finite rings, it is a PID iff it is an integral domain.
            # Thus, it is NOT a PID iff it is NOT an integral domain.
            neg_q = not is_domain
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is equipped with a Euclidean function making it a Euclidean domain",
    "¬Q: R is not a Principal Ideal Domain (PID)"
]

N_HYP = 1
NEG_Q_INDEX = 1