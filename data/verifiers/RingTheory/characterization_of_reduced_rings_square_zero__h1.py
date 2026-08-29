import sympy
from sympy import eye, zeros
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_eq(a, b):
    if a is b:
        return True
    try:
        if a == b:
            return True
    except Exception:
        pass
    try:
        if hasattr(a, 'equals') and callable(a.equals):
            if a.equals(b):
                return True
    except Exception:
        pass
    return False

def get_elements(witness):
    if hasattr(witness, 'elements'):
        return list(witness.elements)
    elif hasattr(witness, '__iter__'):
        return list(witness)
    else:
        raise ValueError("Cannot get elements from witness")

def get_zero(witness, elements):
    if hasattr(witness, 'zero'):
        return witness.zero
    # In any distributive structure, 0 is the unique element e such that e * x = e for all x
    for e in elements:
        is_zero = True
        for x in elements:
            try:
                if hasattr(witness, 'mul'):
                    p = witness.mul(e, x)
                else:
                    p = e * x
                if not is_eq(p, e):
                    is_zero = False
                    break
            except Exception:
                is_zero = False
                break
        if is_zero:
            return e
    return 0

def is_nilpotent(witness, x, zero, max_deg=15):
    # Check for nilpotency in potentially non-associative rings
    S = {1: [x]}
    for n in range(2, max_deg + 1):
        S[n] = []
        for i in range(1, n):
            j = n - i
            for a in S[i]:
                for b in S[j]:
                    try:
                        if hasattr(witness, 'mul'):
                            prod = witness.mul(a, b)
                        else:
                            prod = a * b
                        S[n].append(prod)
                    except Exception:
                        pass
        
        for item in S[n]:
            if is_eq(item, zero):
                return True
                
        if not S[n]:
            break
            
        # Keep only unique elements to prevent exponential blowup
        unique = []
        for item in S[n]:
            if not any(is_eq(item, u) for u in unique):
                unique.append(item)
        S[n] = unique
        
    return False

def check_is_reduced(witness, elements, zero):
    if hasattr(witness, 'is_reduced'):
        if callable(witness.is_reduced):
            return witness.is_reduced()
        return witness.is_reduced
    
    max_d = min(15, len(elements) + 2)
    for x in elements:
        if is_eq(x, zero):
            continue
        if is_nilpotent(witness, x, zero, max_deg=max_d):
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        elements = get_elements(witness)
        zero = get_zero(witness, elements)
        
        # Check if x^2 == 0 implies x == 0
        sq_zero_implies_zero = True
        for x in elements:
            try:
                if hasattr(witness, 'mul'):
                    x2 = witness.mul(x, x)
                else:
                    x2 = x * x
            except Exception:
                x2 = x * x
                
            if is_eq(x2, zero) and not is_eq(x, zero):
                sq_zero_implies_zero = False
                break
                
        # Check if R is a reduced ring (has no non-zero nilpotent elements)
        is_red = check_is_reduced(witness, elements, zero)
        
        # The conjecture claims: R is reduced iff (x^2 = 0 implies x = 0)
        # The negated conclusion is True when this equivalence fails.
        neg_q = bool(is_red != sq_zero_implies_zero)
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence 'R is reduced iff x^2 = 0 implies x = 0' fails at the witness"
]

N_HYP = 0
NEG_Q_INDEX = 0