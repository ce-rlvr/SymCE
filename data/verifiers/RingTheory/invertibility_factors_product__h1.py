import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_ideal(obj):
    """Check if the object represents an ideal."""
    if isinstance(obj, dict) and 'is_ideal' in obj:
        return bool(obj['is_ideal'])
    if hasattr(obj, 'is_ideal'):
        val = getattr(obj, 'is_ideal')
        return bool(val()) if callable(val) else bool(val)
    # Duck-typing for SymPy ideals
    if hasattr(obj, 'ring') and hasattr(obj, 'gens'):
        return True
    raise ValueError("Cannot determine if object is an ideal")

def check_invertible(obj):
    """Check if the ideal is invertible."""
    if isinstance(obj, dict) and 'is_invertible' in obj:
        return bool(obj['is_invertible'])
    if hasattr(obj, 'is_invertible'):
        val = getattr(obj, 'is_invertible')
        return bool(val()) if callable(val) else bool(val)
    # For SymPy polynomial rings (which are UFDs), an ideal is invertible iff it is principal
    if hasattr(obj, 'gens'):
        gens = [g for g in obj.gens if g != 0]
        if len(gens) <= 1:
            return True
        try:
            if hasattr(obj, 'ring'):
                gb = sympy.groebner(gens, *obj.ring.gens)
            else:
                gb = sympy.groebner(gens)
            return len(gb) <= 1
        except Exception:
            pass
    raise ValueError("Cannot determine if object is invertible")

def conditions(witness) -> list[bool]:
    try:
        # 1. Check if witness is a direct boolean dictionary of properties
        if isinstance(witness, dict) and any(k in witness for k in ['I_is_ideal', 'is_ideal_I']):
            h1 = bool(witness.get('I_is_ideal', witness.get('is_ideal_I', False)))
            h2 = bool(witness.get('J_is_ideal', witness.get('is_ideal_J', False)))
            h3 = bool(witness.get('IJ_is_invertible', witness.get('is_invertible_IJ', False)))
            I_inv = bool(witness.get('I_is_invertible', witness.get('is_invertible_I', True)))
            J_inv = bool(witness.get('J_is_invertible', witness.get('is_invertible_J', True)))
            return [h1, h2, h3, not (I_inv and J_inv)]
            
        # 2. Check if witness provides the ideal objects directly
        if isinstance(witness, dict):
            I = witness['I']
            J = witness['J']
            IJ = witness['IJ'] if 'IJ' in witness else I * J
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                I, J = witness
                IJ = I * J
            elif len(witness) == 3:
                I, J, IJ = witness
            else:
                raise ValueError("Witness tuple must be of length 2 or 3")
        else:
            I = witness.I
            J = witness.J
            IJ = getattr(witness, 'IJ', I * J if hasattr(I, '__mul__') else None)
            
        h1 = check_ideal(I)
        h2 = check_ideal(J)
        h3 = check_invertible(IJ)
        
        I_inv = check_invertible(I)
        J_inv = check_invertible(J)
        neg_q = not (I_inv and J_inv)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "H_3: The product ideal IJ is an invertible ideal",
    "¬Q: At least one of I or J is not an invertible ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3