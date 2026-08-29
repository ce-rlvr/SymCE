import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: Hom_R(M1, M2) = {0}",
    "H_3: Hom_R(M2, M1) = {0}",
    "¬Q: End_R(M1 \oplus M2) is not isomorphic to End_R(M1) \times End_R(M2)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1 = h2 = h3 = neg_q = False
    
    # Duck-typing for mock objects or dictionaries
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_ring', witness.get('H1', False)))
            h2 = bool(witness.get('hom_M1_M2_zero', witness.get('H2', False)))
            h3 = bool(witness.get('hom_M2_M1_zero', witness.get('H3', False)))
            q = bool(witness.get('end_isomorphic', witness.get('Q', True)))
            neg_q = not q
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Duck-typing for objects with attributes
    try:
        if hasattr(witness, 'is_ring'):
            val = witness.is_ring
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'H1'):
            val = witness.H1
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    try:
        if hasattr(witness, 'hom_M1_M2_zero'):
            val = witness.hom_M1_M2_zero
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'H2'):
            val = witness.H2
            h2 = bool(val() if callable(val) else val)
    except Exception:
        pass

    try:
        if hasattr(witness, 'hom_M2_M1_zero'):
            val = witness.hom_M2_M1_zero
            h3 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'H3'):
            val = witness.H3
            h3 = bool(val() if callable(val) else val)
    except Exception:
        pass

    try:
        if hasattr(witness, 'end_isomorphic'):
            val = witness.end_isomorphic
            q = bool(val() if callable(val) else val)
            neg_q = not q
        elif hasattr(witness, 'Q'):
            val = witness.Q
            q = bool(val() if callable(val) else val)
            neg_q = not q
    except Exception:
        pass

    # If the witness is a tuple (R, M1, M2) of custom objects
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        R, M1, M2 = witness
        
        try:
            if hasattr(R, 'is_ring'):
                h1 = bool(R.is_ring() if callable(R.is_ring) else R.is_ring)
            elif hasattr(R, 'is_Ring'):
                h1 = bool(R.is_Ring() if callable(R.is_Ring) else R.is_Ring)
            else:
                h1 = True
        except Exception:
            pass
            
        try:
            if hasattr(M1, 'hom'):
                hom12 = M1.hom(M2)
            elif hasattr(R, 'hom'):
                hom12 = R.hom(M1, M2)
            else:
                hom12 = None
                
            if hom12 is not None:
                if hasattr(hom12, 'is_zero'):
                    h2 = bool(hom12.is_zero() if callable(hom12.is_zero) else hom12.is_zero)
                else:
                    h2 = (hom12 == 0 or hom12 == [0] or hom12 == {0} or hom12 == set())
        except Exception:
            pass
            
        try:
            if hasattr(M2, 'hom'):
                hom21 = M2.hom(M1)
            elif hasattr(R, 'hom'):
                hom21 = R.hom(M2, M1)
            else:
                hom21 = None
                
            if hom21 is not None:
                if hasattr(hom21, 'is_zero'):
                    h3 = bool(hom21.is_zero() if callable(hom21.is_zero) else hom21.is_zero)
                else:
                    h3 = (hom21 == 0 or hom21 == [0] or hom21 == {0} or hom21 == set())
        except Exception:
            pass
            
        try:
            if hasattr(M1, 'direct_sum'):
                M12 = M1.direct_sum(M2)
            elif hasattr(M1, '__add__'):
                M12 = M1 + M2
            else:
                M12 = None
                
            if M12 is not None and hasattr(M12, 'end'):
                end12 = M12.end()
                end1 = M1.end()
                end2 = M2.end()
                if hasattr(end1, 'direct_product'):
                    prod = end1.direct_product(end2)
                elif hasattr(end1, '__mul__'):
                    prod = end1 * end2
                else:
                    prod = None
                    
                if prod is not None and hasattr(end12, 'is_isomorphic'):
                    q = bool(end12.is_isomorphic(prod))
                    neg_q = not q
        except Exception:
            pass

    return [h1, h2, h3, neg_q]