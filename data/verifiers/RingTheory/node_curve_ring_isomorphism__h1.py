import sympy
from sympy import *

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        char_F = None
        has_2_torsion = False
        
        if isinstance(witness, int):
            char_F = abs(witness)
            has_2_torsion = (char_F % 2 == 0 and char_F != 0)
        elif hasattr(witness, 'characteristic'):
            char_F = witness.characteristic()
            if callable(char_F):
                char_F = char_F()
            if hasattr(witness, 'order'):
                order = witness.order
                if callable(order):
                    order = order()
                has_2_torsion = (order % 2 == 0)
            else:
                has_2_torsion = (char_F == 2)
        elif hasattr(witness, 'char'):
            char_F = witness.char
            if callable(char_F):
                char_F = char_F()
            if getattr(witness, 'is_Field', False) or getattr(witness, 'is_Domain', False):
                has_2_torsion = (char_F == 2)
            else:
                has_2_torsion = (char_F % 2 == 0 and char_F != 0)
        else:
            n = int(witness)
            char_F = abs(n)
            has_2_torsion = (char_F % 2 == 0 and char_F != 0)
            
        if char_F is None:
            return [False, False]
            
        h1_ok = (char_F != 2)
        neg_q_ok = has_2_torsion
        
        return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: The characteristic of F is not 2",
    "not Q: The factor ring F(x, y)/(y^2 - x^2(x+1)) is NOT isomorphic to the subring of F(t) where p(1) = p(-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1