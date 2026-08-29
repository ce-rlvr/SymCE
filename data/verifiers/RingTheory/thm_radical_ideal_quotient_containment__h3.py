import sympy
from sympy import symbols
from sympy.abc import x, y, z
import itertools

# Top-level setup
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_elements(obj):
    if hasattr(obj, 'elements'):
        el = obj.elements
        if callable(el):
            return list(el())
        return list(el)
    elif isinstance(obj, (list, set, tuple)):
        return list(obj)
    raise ValueError("Cannot get elements")

def is_commutative_ring(R):
    try:
        elements = get_elements(R)
        zero = R.zero
        for a in elements:
            if R.add(a, zero) != a: return False
            if R.add(zero, a) != a: return False
            for b in elements:
                if R.add(a, b) != R.add(b, a): return False
                if R.mul(a, b) != R.mul(b, a): return False
                for c in elements:
                    if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                    if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
        for a in elements:
            has_inv = False
            for b in elements:
                if R.add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
        return True
    except Exception:
        return False

def is_ideal(R, I):
    try:
        elements = get_elements(R)
        I_elements = get_elements(I)
        zero = R.zero
        if zero not in I_elements: return False
        for a in I_elements:
            for b in I_elements:
                minus_b = None
                for e in elements:
                    if R.add(b, e) == zero:
                        minus_b = e
                        break
                if minus_b is None: return False
                if R.add(a, minus_b) not in I_elements: return False
        for a in I_elements:
            for r in elements:
                if R.mul(r, a) not in I_elements: return False
                if R.mul(a, r) not in I_elements: return False
        return True
    except Exception:
        return False

def radical(R, J):
    elements = get_elements(R)
    J_elements = get_elements(J)
    rad = []
    for r in elements:
        current = r
        found = False
        for n in range(1, len(elements) + 2):
            if current in J_elements:
                found = True
                break
            current = R.mul(current, r)
        if found:
            rad.append(r)
    return rad

def ideal_quotient(R, I, x):
    elements = get_elements(R)
    I_elements = get_elements(I)
    try:
        x_elements = get_elements(x)
    except Exception:
        x_elements = [x]
    
    quotient = []
    for r in elements:
        if all(R.mul(r, xe) in I_elements for xe in x_elements):
            quotient.append(r)
    return quotient

def check_subset(A, B):
    try:
        A_elements = get_elements(A)
    except Exception:
        A_elements = A
    try:
        B_elements = get_elements(B)
    except Exception:
        B_elements = B
    return all(elem in B_elements for elem in A_elements)

def conditions(witness):
    try:
        R, I, x = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_commutative_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(R, I)
    except Exception:
        h2 = False
        
    try:
        # \sqrt{(I : x)}
        I_colon_x = ideal_quotient(R, I, x)
        rad_I_colon_x = radical(R, I_colon_x)
        
        # (\sqrt{I} : x)
        rad_I = radical(R, I)
        rad_I_colon_x_2 = ideal_quotient(R, rad_I, x)
        
        # Conclusion: \sqrt{(I : x)} \subseteq (\sqrt{I} : x)
        # Negated conclusion: NOT subset
        neg_q = not check_subset(rad_I_colon_x, rad_I_colon_x_2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The radical of the ideal quotient \\sqrt{(I : x)} is not a subset of (\\sqrt{I} : x)"
]

N_HYP = 2
NEG_Q_INDEX = 2