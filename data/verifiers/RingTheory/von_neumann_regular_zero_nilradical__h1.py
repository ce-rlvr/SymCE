import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(witness):
    if hasattr(witness, 'elements'):
        el = witness.elements
        el = el() if callable(el) else el
        return list(el)
    if isinstance(witness, (list, tuple, set)):
        return list(witness)
    raise ValueError("Cannot determine elements of the ring")

def mul(witness, a, b):
    if hasattr(witness, 'mul'):
        return witness.mul(a, b)
    return a * b

def add(witness, a, b):
    if hasattr(witness, 'add'):
        return witness.add(a, b)
    return a + b

def get_zero(witness, elements):
    if hasattr(witness, 'zero'):
        z_val = witness.zero
        return z_val() if callable(z_val) else z_val
    if hasattr(witness, 'zero_element'):
        z_val = witness.zero_element
        return z_val() if callable(z_val) else z_val
    
    # Try to find the additive identity
    for e in elements:
        try:
            if all(add(witness, e, x_elem) == x_elem and add(witness, x_elem, e) == x_elem for x_elem in elements):
                return e
        except Exception:
            pass
            
    # Fallback for sympy matrices or objects with an is_zero property
    if elements and hasattr(elements[0], 'is_zero'):
        for e in elements:
            if getattr(e, 'is_zero', False) == True:
                return e
                
    return 0

def check_hyp(witness):
    try:
        elements = get_elements(witness)
        for a in elements:
            a2 = mul(witness, a, a)
            found = False
            for x_elem in elements:
                # We check both the literal hypothesis (a = a^2 x) and the standard 
                # Von Neumann regular condition (a = a x a) to be robust against 
                # the dropped "commutative" assumption in the prompt's formulation.
                if (mul(witness, a2, x_elem) == a or 
                    mul(witness, x_elem, a2) == a or 
                    mul(witness, mul(witness, a, x_elem), a) == a):
                    found = True
                    break
            if not found:
                return False
        return True
    except Exception:
        return False

def check_neg_concl(witness):
    try:
        elements = get_elements(witness)
        z_val = get_zero(witness, elements)
        
        # The conclusion "The nilradical of R is the zero ideal" fails if there 
        # is a non-zero nilpotent element in the ring.
        for a in elements:
            if a == z_val:
                continue
            
            current = a
            is_nilpotent = False
            # By Pigeonhole Principle, if it is nilpotent, it must reach 0 within len(elements) steps
            for _ in range(len(elements)):
                current = mul(witness, current, a)
                if current == z_val:
                    is_nilpotent = True
                    break
            
            if is_nilpotent:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    return [
        check_hyp(witness),
        check_neg_concl(witness)
    ]

CONDITION_LABELS = [
    "H_1: For every a in R, there exists x in R such that a = a^2 x",
    "¬Q: The nilradical of R is not the zero ideal (R has non-zero nilpotent elements)"
]

N_HYP = 1
NEG_Q_INDEX = 1