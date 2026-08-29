import math
import sympy
from sympy import oo

class FieldExtension:
    """
    Represents a field extension K/Q.
    """
    def __init__(self, degree, is_galois, is_abelian):
        self.degree = degree
        self.is_galois = bool(is_galois)
        self.is_abelian = bool(is_abelian)

# Predefined extensions for the witness namespace
Q_max_abelian = FieldExtension(degree=oo, is_galois=True, is_abelian=True)
Q_algebraic = FieldExtension(degree=oo, is_galois=True, is_abelian=False)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, FieldExtension):
            h1 = witness.is_galois
            h2 = witness.is_abelian
            
            # By the Kronecker-Weber theorem, an extension of Q is a subfield 
            # of a cyclotomic field Q(zeta_n) if and only if it is finite, 
            # Galois, and abelian.
            is_finite = (witness.degree != math.inf and witness.degree != float('inf') and witness.degree != oo)
            is_subfield = is_finite and witness.is_galois and witness.is_abelian
            
            # The conclusion states K is a subfield of a cyclotomic field.
            # neg_q is True when this conclusion FAILS.
            neg_q = not is_subfield
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K/Q is a Galois extension",
    "H_2: Gal(K/Q) is an abelian group",
    "¬Q: K is not a subfield of any cyclotomic field Q(zeta_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2