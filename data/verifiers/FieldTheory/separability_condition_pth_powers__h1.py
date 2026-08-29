import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x
from sympy.polys.domains import FF
from sympy.polys.domains.fractionfield import FractionField

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
O2 = zeros(2,2)
O3 = zeros(3,3)

class FieldExtension:
    def __init__(self, char, is_separable, E_eq_F_Ep):
        self.char = char
        self.is_separable = is_separable
        self.E_eq_F_Ep = E_eq_F_Ep

def conditions(witness) -> list[bool]:
    char = 0
    is_separable = False
    E_eq_F_Ep = False
    
    try:
        if isinstance(witness, dict):
            char = witness.get('char', 0)
            is_separable = witness.get('is_separable', False)
            E_eq_F_Ep = witness.get('E_eq_F_Ep', False)
        elif isinstance(witness, tuple) and len(witness) == 3:
            char, is_separable, E_eq_F_Ep = witness
        elif hasattr(witness, 'char') and hasattr(witness, 'is_separable') and hasattr(witness, 'E_eq_F_Ep'):
            char = witness.char
            is_separable = witness.is_separable
            E_eq_F_Ep = witness.E_eq_F_Ep
        elif hasattr(witness, 'char'):
            char = witness.char
            if isinstance(witness, FractionField):
                is_separable = True
                E_eq_F_Ep = False
            else:
                is_separable = True
                E_eq_F_Ep = True
    except Exception:
        pass

    try:
        h1 = sympy.isprime(int(char))
    except Exception:
        h1 = False

    try:
        neg_q = (bool(is_separable) != bool(E_eq_F_Ep))
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The characteristic of the field F is a prime number p > 0",
    "¬Q: The extension E/F is separable does NOT hold if and only if E = F(E^p)"
]

N_HYP = 1
NEG_Q_INDEX = 1