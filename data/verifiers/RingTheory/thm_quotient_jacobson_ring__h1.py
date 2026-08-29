import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# We provide a few mock objects representing common non-Jacobson rings 
# in case the witness expression uses them directly.
class MockRing:
    def __init__(self, name, is_jacobson):
        self.name = name
        self._is_jacobson = is_jacobson
        
    def __str__(self):
        return self.name

class MockIdeal:
    def __init__(self, ring, is_proper, quotient_is_jacobson):
        self.ring = ring
        self._is_proper = is_proper
        self._quotient_is_jacobson = quotient_is_jacobson

# Standard counterexamples for non-Jacobson rings
Z_local = MockRing("Z_{(p)}", False)
k_power_series = MockRing("k[[x]]", False)

def is_jacobson(ring):
    if hasattr(ring, '_is_jacobson'):
        return ring._is_jacobson
    if hasattr(ring, 'is_jacobson'):
        if callable(ring.is_jacobson):
            return ring.is_jacobson()
        return ring.is_jacobson
        
    if isinstance(ring, str):
        s = ring.replace(" ", "").lower()
        # Formal power series rings
        if '[[' in s or ']]' in s:
            return False
        # Local rings
        if '_{(p)}' in s or '_(p)' in s or 'local' in s:
            return False
        # p-adic integers
        if 'z_p' in s or 'padic' in s:
            return False
        return True
        
    if hasattr(ring, 'is_Field') and ring.is_Field:
        return True
        
    return True

def is_proper_ideal(R, I):
    if hasattr(I, '_is_proper'):
        return I._is_proper
    if hasattr(I, 'is_proper_ideal'):
        if callable(I.is_proper_ideal):
            return I.is_proper_ideal(R)
        return I.is_proper_ideal
        
    if isinstance(I, str):
        s = I.replace(" ", "").lower()
        if s in ['0', '(0)', '{0}']:
            return True
        if s in ['1', '(1)', 'r']:
            return False
        return True
        
    if I == 0:
        return True
    if I == 1:
        return False
        
    return True

def quotient_is_jacobson(R, I):
    if hasattr(I, '_quotient_is_jacobson'):
        return I._quotient_is_jacobson
    if hasattr(R, 'quotient_is_jacobson'):
        if callable(R.quotient_is_jacobson):
            return R.quotient_is_jacobson(I)
        return R.quotient_is_jacobson
        
    is_zero_ideal = False
    if isinstance(I, str):
        s = I.replace(" ", "").lower()
        if s in ['0', '(0)', '{0}']:
            is_zero_ideal = True
    elif I == 0:
        is_zero_ideal = True
        
    if is_zero_ideal:
        return is_jacobson(R)
        
    if isinstance(I, str) and isinstance(R, str):
        I_s = I.replace(" ", "").lower()
        R_s = R.replace(" ", "").lower()
        if I_s == '(x)' and '[[x,y]]' in R_s:
            return False
        if I_s == '(y)' and '[[x,y]]' in R_s:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R', witness.get('ring'))
            I = witness.get('I', witness.get('ideal', 0))
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
        elif hasattr(witness, 'ring') and hasattr(witness, 'ideal'):
            R = witness.ring
            I = witness.ideal
        else:
            if isinstance(witness, str):
                R = witness
                I = "(0)"
            elif hasattr(witness, '_is_jacobson'):
                R = witness
                I = 0
            else:
                return [False, False]
                
        h1 = is_proper_ideal(R, I)
        q = quotient_is_jacobson(R, I)
        
        return [bool(h1), not bool(q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: The quotient ring R/I is not a Jacobson ring"
]

N_HYP = 1
NEG_Q_INDEX = 1