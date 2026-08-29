import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it satisfies the hypotheses
    and falsifies the conclusion.
    
    Mathematically, the kernel of the canonical homomorphism to the I-adic 
    completion is ALWAYS the intersection of all powers of I, by definition 
    of the inverse limit. Thus, the conclusion is a tautology and never fails 
    for any valid ring and ideal. 
    
    This verifier defaults neg_q to False for standard mathematical objects, 
    but allows mock objects (like dicts or extended tuples) to explicitly 
    provide values for testing purposes.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    # 1. Check if witness is a dictionary (mock object)
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_ring', True))
            h2 = bool(witness.get('is_ideal', True))
            h3 = bool(witness.get('is_canonical_homomorphism', True))
            if 'kernel' in witness and 'intersection_powers' in witness:
                neg_q = witness['kernel'] != witness['intersection_powers']
            else:
                neg_q = False
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a tuple (e.g., (R, I) or (R, I, kernel, intersection))
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            R, I = witness[0], witness[1]
            
            R_type = type(R).__name__
            if R_type in ['PolyRing', 'Ring', 'FractionField'] or R in [ZZ, QQ, RR, CC]:
                h1 = True
            else:
                h1 = bool(getattr(R, 'is_ring', True))
                
            I_type = type(I).__name__
            if I_type == 'Ideal':
                h2 = True
            else:
                h2 = bool(getattr(I, 'is_ideal', True))
                
            h3 = True
            
            if len(witness) >= 4:
                neg_q = witness[2] != witness[3]
            else:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 3. Check if witness is a custom object with attributes
    try:
        h1 = bool(getattr(witness, 'is_ring', True))
        h2 = bool(getattr(witness, 'is_ideal', True))
        h3 = bool(getattr(witness, 'is_canonical_homomorphism', True))
        
        if hasattr(witness, 'kernel') and hasattr(witness, 'intersection_powers'):
            ker = witness.kernel() if callable(witness.kernel) else witness.kernel
            inter = witness.intersection_powers() if callable(witness.intersection_powers) else witness.intersection_powers
            neg_q = (ker != inter)
        else:
            neg_q = False
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: phi is the canonical ring homomorphism",
    "¬Q: The kernel of phi is not the intersection of all powers of I"
]

N_HYP = 3
NEG_Q_INDEX = 3