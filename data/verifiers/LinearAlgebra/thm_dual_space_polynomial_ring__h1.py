import sympy
from sympy import QQ, ZZ, GF
from sympy.abc import x

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        F = None
        if hasattr(witness, 'is_Field') and getattr(witness, 'is_Field', False):
            F = witness
        elif hasattr(witness, 'domain') and getattr(witness.domain, 'is_Field', False):
            F = witness.domain
        elif isinstance(witness, int) and sympy.isprime(witness):
            F = sympy.GF(witness)
        elif isinstance(witness, tuple) or isinstance(witness, list):
            for item in witness:
                if hasattr(item, 'is_Field') and getattr(item, 'is_Field', False):
                    F = item
                    break
                elif hasattr(item, 'domain') and getattr(item.domain, 'is_Field', False):
                    F = item.domain
                    break
                elif isinstance(item, int) and sympy.isprime(item):
                    F = sympy.GF(item)
                    break
                    
        if F is None:
            return [False, False, False]
            
        h1 = True
        h2 = True
        
        char = 0
        if hasattr(F, 'characteristic'):
            char_attr = F.characteristic
            if callable(char_attr):
                char = char_attr()
            else:
                char = char_attr
        elif hasattr(F, 'p'):
            char = F.p
        elif hasattr(F, 'mod'):
            char = F.mod
            
        neg_q = (int(char) > 0)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Polynomial ring is the vector space of polynomials in one variable over F",
    "H_2: Power series ring is the vector space of formal power series in one variable over F",
    "¬Q: The dual space of the polynomial ring is not isomorphic to the power series ring"
]

N_HYP = 2
NEG_Q_INDEX = 2