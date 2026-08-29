import sympy as sp
from sympy import sqrt, I, Rational, Integer
import math

def divides(A, B, d):
    """
    Checks if A divides B in Z[sqrt(d)].
    A and B are tuples (x, y) representing x + y*sqrt(d).
    """
    det = A[0]**2 - A[1]**2 * d
    if det == 0:
        return B[0] == 0 and B[1] == 0
    
    num_x2 = B[0]*A[0] - B[1]*A[1]*d
    num_y2 = A[0]*B[1] - A[1]*B[0]
    
    return num_x2 % det == 0 and num_y2 % det == 0

def get_divisors(A, d):
    """
    Returns a list of all divisors of A in Z[sqrt(d)].
    Only works for d < 0 since the unit group is finite.
    """
    norm_A = A[0]**2 - A[1]**2 * d
    if norm_A == 0:
        return []
    
    if d >= 0:
        raise ValueError("Only d < 0 is supported for finite divisor search")
        
    if norm_A > 10000000:
        raise ValueError("Norm too large, preventing timeout")
        
    max_x = int(math.isqrt(norm_A))
    max_y = int(math.isqrt(norm_A // (-d)))
    
    divisors = []
    for x in range(-max_x, max_x + 1):
        for y in range(-max_y, max_y + 1):
            norm_C = x**2 - y**2 * d
            if norm_C == 0 or norm_A % norm_C != 0:
                continue
            C = (x, y)
            if divides(C, A, d):
                divisors.append(C)
    return divisors

def get_common_divisors(A, B, d):
    divs_A = get_divisors(A, d)
    return [C for C in divs_A if divides(C, B, d)]

def has_gcd(A, B, d):
    """
    Checks if A and B have a greatest common divisor in Z[sqrt(d)].
    """
    common_divs = get_common_divisors(A, B, d)
    for g in common_divs:
        is_gcd = True
        for c in common_divs:
            if not divides(c, g, d):
                is_gcd = False
                break
        if is_gcd:
            return True
    return False

def parse_element(elem):
    """
    Parses an element into a tuple (x, y, d) representing x + y*sqrt(d).
    """
    if isinstance(elem, tuple):
        if len(elem) == 3:
            return int(elem[0]), int(elem[1]), int(elem[2])
        if len(elem) == 2:
            return int(elem[0]), int(elem[1]), -5
            
    try:
        elem = sp.sympify(elem)
    except Exception:
        pass

    if hasattr(elem, 'is_Integer') and elem.is_Integer:
        return int(elem), 0, -5
        
    if isinstance(elem, sp.Expr):
        elem = sp.expand(elem)
        x = 0
        y = 0
        d = None
        for term in elem.as_ordered_terms():
            if term.is_Integer:
                x = int(term)
            else:
                coeff, radical = term.as_coeff_Mul()
                
                if radical == sp.I:
                    y = int(coeff)
                    d = -1
                    continue
                    
                if radical.is_Pow and radical.exp == sp.Rational(1, 2):
                    y = int(coeff)
                    d = int(radical.base)
                    continue
                    
                if radical.is_Mul:
                    if sp.I in radical.args:
                        other_args = [arg for arg in radical.args if arg != sp.I]
                        if len(other_args) == 1:
                            other = other_args[0]
                            if other.is_Pow and other.exp == sp.Rational(1, 2):
                                y = int(coeff)
                                d = -int(other.base)
                                continue
                
                raise ValueError(f"Unsupported term: {term}")
        if d is None:
            d = -5
        return x, y, d
        
    raise ValueError("Cannot parse element")

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a_raw = witness.get('a', witness.get('x'))
            b_raw = witness.get('b', witness.get('y'))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                a_raw, b_raw = witness
            elif len(witness) == 3:
                a_raw, b_raw, _ = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        x1, y1, d1 = parse_element(a_raw)
        x2, y2, d2 = parse_element(b_raw)
        
        # Synchronize d if one element is purely real
        if y1 == 0 and y2 != 0:
            d1 = d2
        elif y2 == 0 and y1 != 0:
            d2 = d1
            
        if d1 != d2:
            return [False, False]
            
        d = d1
        if d >= 0:
            return [False, False]
            
        a = (x1, y1)
        b = (x2, y2)
        
        h1 = (a != (0, 0)) and (b != (0, 0))
        
        neg_q = not has_gcd(a, b, d)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "¬Q: a and b DO NOT have a greatest common divisor in R"
]
N_HYP = 1
NEG_Q_INDEX = 1