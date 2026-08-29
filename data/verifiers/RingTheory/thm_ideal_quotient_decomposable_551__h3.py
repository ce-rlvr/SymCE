import math
from functools import reduce
import sympy

# Top-level setup for potential witness references
ZZ = sympy.S.Integers
QQ = sympy.S.Reals
Z2 = sympy.S.Integers
Z3 = sympy.S.Integers
Z4 = sympy.S.Integers
Z6 = sympy.S.Integers

def unwrap(x):
    """Recursively unwrap single-element iterables (like tuples representing principal ideals)."""
    if isinstance(x, str):
        return x
    try:
        if len(x) == 1:
            return unwrap(next(iter(x)))
    except Exception:
        pass
    return x

def is_int(x):
    """Check if a value can be safely treated as an integer."""
    if isinstance(x, int):
        return True
    if isinstance(x, float):
        return x.is_integer()
    if hasattr(x, 'is_integer'):
        try:
            res = x.is_integer
            if res is True or res is False:
                return res
            if callable(res):
                return res()
        except Exception:
            pass
    try:
        return int(x) == float(x)
    except Exception:
        return False

def extract_witness(witness):
    """Extract I, J, and Q_list from various possible witness formats."""
    if isinstance(witness, dict):
        I = witness.get('I')
        J = witness.get('J')
        Q_list = witness.get('Q_list') or witness.get('Qs')
        if I is not None and J is not None and Q_list is not None:
            return I, J, list(Q_list)
    
    if isinstance(witness, (tuple, list)):
        if len(witness) >= 3:
            # If the last element is explicitly a list, it's likely Q_list
            if isinstance(witness[-1], list):
                I = witness[-3]
                J = witness[-2]
                Q_list = witness[-1]
                return I, J, Q_list
            else:
                # Otherwise, assume a flat structure, possibly prefixed by the ring R
                start_idx = 0
                try:
                    if not is_int(unwrap(witness[0])):
                        start_idx = 1
                except Exception:
                    start_idx = 1
                
                if len(witness) >= start_idx + 3:
                    return witness[start_idx], witness[start_idx+1], list(witness[start_idx+2:])
                elif len(witness) == start_idx + 2:
                    return witness[start_idx], witness[start_idx+1], []
                    
    return None, None, None

def conditions(witness) -> list[bool]:
    H1, H2, H3, neg_Q = False, False, False, False
    
    try:
        I, J, Q_list = extract_witness(witness)
        
        if I is not None and J is not None and Q_list is not None:
            I = unwrap(I)
            J = unwrap(J)
            Q_list = [unwrap(q) for q in Q_list]
            
            # We evaluate the conjecture in the ring of integers Z, which is a commutative ring.
            # Ideals in Z are principal and can be represented by their integer generators.
            if is_int(I) and is_int(J) and all(is_int(q) for q in Q_list):
                I_val = int(I)
                J_val = int(J)
                Q_vals = [int(q) for q in Q_list]
                
                # H_1: R is a commutative ring (Z is a commutative ring)
                H1 = True
                # H_2: I is an ideal in R (any integer generates an ideal in Z)
                H2 = True
                # H_3: J is an ideal in R (any integer generates an ideal in Z)
                H3 = True
                
                def ideal_quotient(a, b):
                    """Returns the generator of the ideal quotient (a):(b) in Z."""
                    if b == 0:
                        return 1
                    if a == 0:
                        return 0
                    return abs(a) // math.gcd(a, b)
                
                def ideal_intersection(ideals):
                    """Returns the generator of the intersection of a list of ideals in Z."""
                    if not ideals:
                        return 1
                    def lcm(x, y):
                        if x == 0 and y == 0:
                            return 0
                        return abs(x * y) // math.gcd(x, y)
                    return reduce(lcm, ideals)
                
                LHS = ideal_quotient(I_val, J_val)
                rhs_ideals = [ideal_quotient(q, J_val) for q in Q_vals]
                RHS = ideal_intersection(rhs_ideals)
                
                # ¬Q: The ideal quotient (I:J) is NOT equal to the intersection \bigcap_{i=1}^n (Q_i:J)
                neg_Q = (abs(LHS) != abs(RHS))
    except Exception:
        pass
        
    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal in R",
    "H_3: J is an ideal in R",
    "¬Q: The ideal quotient (I:J) is not equal to the intersection \\bigcap_{i=1}^n (Q_i:J)"
]

N_HYP = 3
NEG_Q_INDEX = 3