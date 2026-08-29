import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: B is the set of all idempotent elements of R",
    "H_3: Addition on B is defined as x (+) y = x + y - 2xy",
    "¬Q: B does not form a Boolean ring under (+) and standard multiplication"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_ring_api(R):
    if hasattr(R, 'elements'):
        try:
            elements = list(R.elements)
        except Exception:
            elements = None
    else:
        elements = None
        
    if elements is not None:
        if hasattr(R, 'add'):
            add = R.add
        else:
            add = lambda x, y: x + y
            
        if hasattr(R, 'mul'):
            mul = R.mul
        else:
            mul = lambda x, y: x * y
            
        if hasattr(R, 'zero'):
            zero = R.zero
        else:
            zero = None
            for e in elements:
                try:
                    if all(add(e, x) == x for x in elements):
                        zero = e
                        break
                except Exception:
                    pass
                    
        if hasattr(R, 'one'):
            one = R.one
        else:
            one = None
            for e in elements:
                try:
                    if all(mul(e, x) == x for x in elements):
                        one = e
                        break
                except Exception:
                    pass
                    
        def neg(x):
            for a in elements:
                try:
                    if add(x, a) == zero:
                        return a
                except Exception:
                    pass
            return x
            
        def plus(x, y):
            xy = mul(x, y)
            two_xy = add(xy, xy)
            return add(add(x, y), neg(two_xy))
            
        idemps = []
        for x in elements:
            try:
                if mul(x, x) == x:
                    idemps.append(x)
            except Exception:
                pass
                
        return elements, add, mul, zero, one, idemps, plus
        
    else:
        # SymPy ring fallback
        zero = getattr(R, 'zero', 0)
        one = getattr(R, 'one', 1)
        add = lambda x, y: x + y
        mul = lambda x, y: x * y
        idemps = [zero, one]
        def plus(x, y):
            return x + y - 2*x*y
        return None, add, mul, zero, one, idemps, plus

def is_comm_ring_with_id(elements, add, mul, zero, one):
    if elements is None:
        return True 
        
    if zero is None or one is None:
        return False
        
    try:
        for a in elements:
            if not (add(a, zero) == a) or not (add(zero, a) == a): return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                if not (add(a, b) == add(b, a)): return False
                for c in elements:
                    if not (add(add(a, b), c) == add(a, add(b, c))): return False
                    
        for a in elements:
            if not (mul(a, one) == a) or not (mul(one, a) == a): return False
            for b in elements:
                if not (mul(a, b) == mul(b, a)): return False
                for c in elements:
                    if not (mul(mul(a, b), c) == mul(a, mul(b, c))): return False
                    
        for a in elements:
            for b in elements:
                for c in elements:
                    if not (mul(a, add(b, c)) == add(mul(a, b), mul(a, c))): return False
                    
        return True
    except Exception:
        return False

def check_boolean_ring(B, plus, mul, zero):
    if not B:
        return False
    try:
        for a in B:
            for b in B:
                if not any(plus(a, b) == x for x in B): return False
                
        for a in B:
            for b in B:
                for c in B:
                    if not (plus(plus(a, b), c) == plus(a, plus(b, c))): return False
                    
        for a in B:
            for b in B:
                if not (plus(a, b) == plus(b, a)): return False
                
        for a in B:
            if not (plus(a, zero) == a): return False
            if not (plus(zero, a) == a): return False
            
        for a in B:
            has_inv = False
            for b in B:
                if plus(a, b) == zero and plus(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        for a in B:
            for b in B:
                if not any(mul(a, b) == x for x in B): return False
                
        for a in B:
            for b in B:
                for c in B:
                    if not (mul(mul(a, b), c) == mul(a, mul(b, c))): return False
                    
        for a in B:
            for b in B:
                for c in B:
                    if not (mul(a, plus(b, c)) == plus(mul(a, b), mul(a, c))): return False
                    if not (mul(plus(a, b), c) == plus(mul(a, c), mul(b, c))): return False
                    
        for a in B:
            if not (mul(a, a) == a): return False
            
        has_one = False
        for e in B:
            is_one = True
            for a in B:
                if not (mul(e, a) == a) or not (mul(a, e) == a):
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) >= 3:
            R, B_wit, plus_wit = witness[:3]
        elif len(witness) == 2:
            R, B_wit = witness
            plus_wit = None
        elif len(witness) == 1:
            R = witness[0]
            B_wit = None
            plus_wit = None
        else:
            R = witness
            B_wit = None
            plus_wit = None
    else:
        R = witness
        B_wit = None
        plus_wit = None
        
    elements, add, mul, zero, one, idemps, plus = get_ring_api(R)
    
    try:
        if elements is not None:
            h1_ok = is_comm_ring_with_id(elements, add, mul, zero, one)
        else:
            h1_ok = getattr(R, 'is_commutative', True)
    except Exception:
        h1_ok = False
        
    try:
        if B_wit is not None:
            h2_ok = (sorted(list(B_wit), key=str) == sorted(idemps, key=str))
        else:
            h2_ok = True
    except Exception:
        h2_ok = False
        
    try:
        if plus_wit is not None:
            h3_ok = True
            for x in idemps:
                for y in idemps:
                    if plus_wit(x, y) != plus(x, y):
                        h3_ok = False
                        break
        else:
            h3_ok = True
    except Exception:
        h3_ok = False
        
    try:
        is_bool_ring = check_boolean_ring(idemps, plus, mul, zero)
        neg_q = not is_bool_ring
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q]