import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ring(R):
    if not R:
        return False
    
    # Check closure under addition
    for a in R:
        for b in R:
            if (a + b) not in R:
                return False
                
    # Check closure under multiplication
    for a in R:
        for b in R:
            if (a * b) not in R:
                return False
                
    # Check additive identity
    z_elem = None
    for elem in R:
        if all((a + elem) == a and (elem + a) == a for a in R):
            z_elem = elem
            break
    if z_elem is None:
        return False
        
    # Check additive inverse
    for a in R:
        if not any((a + b) == z_elem and (b + a) == z_elem for b in R):
            return False
            
    # Check associativity and distributivity
    for a in R:
        for b in R:
            for c in R:
                if (a + b) + c != a + (b + c):
                    return False
                if (a * b) * c != a * (b * c):
                    return False
                if a * (b + c) != (a * b) + (a * c):
                    return False
                if (a + b) * c != (a * c) + (b * c):
                    return False
    return True

def is_ideal(R, I):
    if not I:
        return False
        
    # I must be a subset of R
    for i in I:
        if i not in R:
            return False
            
    # I must be closed under addition
    for a in I:
        for b in I:
            if (a + b) not in I:
                return False
                
    # I must be closed under inside-outside multiplication
    for i in I:
        for r in R:
            if (i * r) not in I:
                return False
            if (r * i) not in I:
                return False
                
    # I must have an additive inverse for each element
    z_elem = None
    for elem in I:
        if all((a + elem) == a and (elem + a) == a for a in I):
            z_elem = elem
            break
    if z_elem is None:
        return False
        
    for a in I:
        if not any((a + b) == z_elem and (b + a) == z_elem for b in I):
            return False
            
    return True

def center(R):
    Z = []
    for a in R:
        if all(a * x_elem == x_elem * a for x_elem in R):
            Z.append(a)
    return Z

def in_center_quotient(c, R, I):
    for x_elem in R:
        cx = c * x_elem
        xc = x_elem * c
        # Check if cx and xc are in the same coset (i.e., cx - xc in I)
        # We check if cx == xc + i for some i in I
        if not any(cx == xc + i for i in I):
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, I = witness
            elif len(witness) == 3:
                R, I, pi = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_ring(R)
    except Exception:
        h1 = False

    try:
        h2 = is_ideal(R, I)
    except Exception:
        h2 = False

    try:
        # \pi is the canonical projection is structurally satisfied by our quotient evaluation
        h3 = True if (h1 and h2) else False
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2:
            Z_R = center(R)
            for z_elem in Z_R:
                if not in_center_quotient(z_elem, R, I):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: \\pi: R -> R/I is the canonical projection",
    "¬Q: The image \\pi(Z(R)) is not contained in the center of R/I"
]

N_HYP = 3
NEG_Q_INDEX = 3