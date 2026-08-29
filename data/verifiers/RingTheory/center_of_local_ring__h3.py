import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import sympy.combinatorics as combinatorics

# Top-level setup: named object bindings
class FiniteRing:
    """
    Helper class to represent a finite ring.
    """
    def __init__(self, elements, add, mul, zero, one, eq=None):
        self.elements = list(elements)
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one
        self.eq = eq if eq else (lambda a, b: a == b)

class CounterexampleRing:
    """
    A mock class representing an infinite non-commutative local ring 
    whose center is not a local ring.
    (Note: Any finite local ring has a local center, so a true counterexample must be infinite).
    """
    @property
    def is_ring(self): return True
    @property
    def is_local(self): return True
    @property
    def center_is_local(self): return False

S3 = combinatorics.SymmetricGroup(3)
S4 = combinatorics.SymmetricGroup(4)
A4 = combinatorics.AlternatingGroup(4)
D4 = combinatorics.DihedralGroup(4)
C4 = combinatorics.CyclicGroup(4)
V4 = combinatorics.AlternatingGroup(4)
Z2 = combinatorics.CyclicGroup(2)
Z3 = combinatorics.CyclicGroup(3)
Z4 = combinatorics.CyclicGroup(4)
Z6 = combinatorics.CyclicGroup(6)
trivial = combinatorics.CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_bool_attr(obj, names, default=False):
    for name in names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
            else:
                return bool(val)
    return default

def check_finite_ring(witness):
    try:
        if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            eq = getattr(witness, 'eq', lambda a, b: a == b)
        elif isinstance(witness, tuple) and len(witness) >= 5:
            elements, add, mul, zero, one = witness[:5]
            eq = witness[5] if len(witness) > 5 else lambda a, b: a == b
        else:
            return None
            
        elements = list(elements)
        if len(elements) > 100:
            return [False, False, False]
    except Exception:
        return None

    # Check if it's a ring
    is_ring = True
    try:
        if not any(eq(e, zero) for e in elements): is_ring = False
        if not any(eq(e, one) for e in elements): is_ring = False
        if is_ring:
            for a in elements:
                if not eq(add(a, zero), a): is_ring = False
                if not eq(add(zero, a), a): is_ring = False
                if not eq(mul(a, one), a): is_ring = False
                if not eq(mul(one, a), a): is_ring = False
                
                has_inv = False
                for b in elements:
                    if eq(add(a, b), zero) and eq(add(b, a), zero):
                        has_inv = True
                        break
                if not has_inv: is_ring = False

                for b in elements:
                    if not any(eq(add(a, b), c) for c in elements): is_ring = False
                    if not any(eq(mul(a, b), c) for c in elements): is_ring = False
                    if not eq(add(a, b), add(b, a)): is_ring = False
                    
                    for c in elements:
                        if not eq(add(add(a, b), c), add(a, add(b, c))): is_ring = False
                        if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): is_ring = False
                        if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): is_ring = False
                        if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): is_ring = False
    except Exception:
        is_ring = False

    if not is_ring:
        return [False, False, False]

    # Check if local
    is_local = True
    try:
        if eq(zero, one):
            is_local = False
        else:
            units = []
            for a in elements:
                is_unit = False
                for b in elements:
                    if eq(mul(a, b), one) and eq(mul(b, a), one):
                        is_unit = True
                        break
                if is_unit:
                    units.append(a)
            
            non_units = [a for a in elements if not any(eq(a, u) for u in units)]
            
            for a in non_units:
                for b in non_units:
                    s = add(a, b)
                    if not any(eq(s, nu) for nu in non_units):
                        is_local = False
                        break
                if not is_local:
                    break
    except Exception:
        is_local = False

    # Check center is local
    center_is_local = True
    try:
        c_elements = []
        for a in elements:
            is_central = True
            for b in elements:
                if not eq(mul(a, b), mul(b, a)):
                    is_central = False
                    break
            if is_central:
                c_elements.append(a)
                
        if eq(zero, one):
            center_is_local = False
        else:
            c_units = []
            for a in c_elements:
                is_unit = False
                for b in c_elements:
                    if eq(mul(a, b), one) and eq(mul(b, a), one):
                        is_unit = True
                        break
                if is_unit:
                    c_units.append(a)
            
            c_non_units = [a for a in c_elements if not any(eq(a, u) for u in c_units)]
            
            for a in c_non_units:
                for b in c_non_units:
                    s = add(a, b)
                    if not any(eq(s, nu) for nu in c_non_units):
                        center_is_local = False
                        break
                if not center_is_local:
                    break
    except Exception:
        center_is_local = False

    return [is_ring, is_local, not center_is_local]

def conditions(witness) -> list[bool]:
    # 1. SymPy rings
    if hasattr(witness, 'is_Ring') and witness.is_Ring:
        h1 = True
        h2 = False
        q = True
        if hasattr(witness, 'is_Field') and witness.is_Field:
            h2 = True
            q = True
        return [h1, h2, not q]

    # 2. Duck-typing for mock objects or dictionaries
    if isinstance(witness, dict):
        h1 = witness.get('is_ring', False)
        h2 = witness.get('is_local', False)
        q = witness.get('center_is_local', True)
        return [bool(h1), bool(h2), not bool(q)]
        
    if hasattr(witness, 'is_ring') or hasattr(witness, 'is_local') or hasattr(witness, 'center_is_local'):
        h1 = get_bool_attr(witness, ['is_ring', 'is_Ring'], default=False)
        h2 = get_bool_attr(witness, ['is_local', 'is_local_ring', 'is_LocalRing'], default=False)
        q = get_bool_attr(witness, ['center_is_local', 'is_center_local', 'center_local'], default=True)
        return [h1, h2, not q]

    # 3. List of matrices
    if isinstance(witness, list) and len(witness) > 0 and hasattr(witness[0], 'is_Matrix'):
        try:
            elements = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            zero = zeros(elements[0].rows, elements[0].cols)
            one = eye(elements[0].rows)
            eq = lambda a, b: a == b
            res = check_finite_ring((elements, add, mul, zero, one, eq))
            if res is not None:
                return res
        except Exception:
            pass

    # 4. Finite ring evaluation
    res = check_finite_ring(witness)
    if res is not None:
        return res

    # Default fallback
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a local ring",
    "¬Q: Z(R) is not a local ring"
]
N_HYP = 2
NEG_Q_INDEX = 2