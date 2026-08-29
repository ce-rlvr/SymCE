import math
import sympy
from sympy import Symbol

# Top-level setup for potential witness expressions
Z = Symbol('Z')
ZZ = Symbol('ZZ')
Q = Symbol('Q')
R = Symbol('R')
C = Symbol('C')

def extract_int(x):
    if isinstance(x, (list, tuple, set)):
        if len(x) == 1:
            return extract_int(list(x)[0])
        elif len(x) == 0:
            return 0
        raise ValueError
    if isinstance(x, str):
        s = x.replace('Z', '').replace('z', '').strip()
        if s == '':
            return 1
        elif s == '-':
            return -1
        return int(s)
    if hasattr(x, 'as_coeff_Mul'):
        coeff, _ = x.as_coeff_Mul()
        return int(coeff)
    return int(x)

def evaluate_witness(witness):
    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            r = 0
            i = extract_int(witness[0])
            j = extract_int(witness[1])
        elif len(witness) == 3:
            w0 = witness[0]
            if str(w0) in ['Z', 'ZZ', 'ℤ', 'Integers', 'S.Integers'] or w0 is None:
                r = 0
            else:
                r = extract_int(w0)
            i = extract_int(witness[1])
            j = extract_int(witness[2])
        else:
            raise ValueError("Witness must be a tuple of length 2 or 3")
    else:
        raise ValueError("Witness must be a tuple or list")

    is_ring = True
    
    if r == 0:
        is_finite = (i != 0) and (j != 0)
        if not is_finite:
            neg_q = True
        else:
            i_abs = abs(i)
            j_abs = abs(j)
            lcm_val = (i_abs * j_abs) // math.gcd(i_abs, j_abs)
            neg_q = lcm_val != (i_abs * j_abs)
    else:
        r_abs = abs(r)
        is_finite = True
        a = math.gcd(i, r_abs)
        b = math.gcd(j, r_abs)
        lcm_val = (a * b) // math.gcd(a, b)
        neg_q = lcm_val != (a * b)
        
    return is_ring, is_finite, neg_q

def conditions(witness) -> list[bool]:
    try:
        is_ring, is_finite, neg_q = evaluate_witness(witness)
    except Exception:
        is_ring = False
        is_finite = False
        neg_q = False
        
    return [is_ring, is_finite, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: The quotient rings R/I and R/J are finite",
    "¬Q: The quotient ring R/(I \\cap J) is not finite, or its cardinality is not |R/I| \\times |R/J|"
]

N_HYP = 2
NEG_Q_INDEX = 2