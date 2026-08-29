import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Standard bindings
Z = ZZ
Q = QQ

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Parse witness: can be a tuple (R, I), an Ideal object, or just the ideal generators (assuming R=ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'ring'):
            R = witness.ring
            I = witness
        else:
            R = sympy.ZZ
            I = witness
            
        # Check H1: R is a ring with identity
        if hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        elif hasattr(R, 'is_ring') and R.is_ring:
            h1 = True
        elif hasattr(R, 'one') and R.one is not None:
            h1 = True
        elif R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
        elif R == sympy.ZZ or R == sympy.QQ:
            h1 = True
            
        # Check neg_Q: I contains a unit of R
        # An ideal contains a unit if and only if it contains the identity element (1).
        if R == sympy.ZZ or R == sympy.S.Integers:
            if isinstance(I, (list, tuple, set)):
                g = sympy.igcd(*I)
                neg_q = (abs(g) == 1)
            else:
                neg_q = (abs(I) == 1)
        elif R == sympy.QQ or R == sympy.S.Rationals:
            if isinstance(I, (list, tuple, set)):
                neg_q = any(val != 0 for val in I)
            else:
                neg_q = (I != 0)
        elif hasattr(I, 'contains') and hasattr(R, 'one'):
            neg_q = bool(I.contains(R.one))
        elif hasattr(R, 'ideal'):
            if isinstance(I, (list, tuple, set)):
                ideal_obj = R.ideal(*I)
            else:
                ideal_obj = R.ideal(I)
            neg_q = bool(ideal_obj.contains(R.one))
        else:
            # Fallback for other rings (e.g., matrix rings)
            if isinstance(I, (list, tuple, set)):
                neg_q = 1 in I or (hasattr(R, 'one') and R.one in I)
            else:
                neg_q = (I == 1 or (hasattr(R, 'one') and I == R.one))
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "¬Q: I contains at least one unit of R"
]

N_HYP = 1
NEG_Q_INDEX = 1