import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import totient

class InfiniteCyclicGroup:
    @property
    def is_cyclic(self):
        return True
    
    def order(self):
        return sympy.oo
        
    @property
    def is_finite(self):
        return False

Z = InfiniteCyclicGroup()
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if witness is sympy.S.Integers or isinstance(witness, InfiniteCyclicGroup):
            h1 = True
        elif hasattr(witness, 'generators') and len(witness.generators) == 1 and type(witness).__name__ == 'FreeGroup':
            h1 = True
        else:
            h1 = bool(witness.is_cyclic)
    except Exception:
        h1 = False

    try:
        if witness is sympy.S.Integers or isinstance(witness, InfiniteCyclicGroup):
            n = sympy.oo
            aut_order = 2
        elif hasattr(witness, 'generators') and len(witness.generators) == 1 and type(witness).__name__ == 'FreeGroup':
            n = sympy.oo
            aut_order = 2
        else:
            n = witness.order()
            if getattr(witness, 'is_cyclic', False):
                aut_order = totient(n)
            else:
                aut_order = -1
                
        if n == sympy.oo:
            neg_q = True
        else:
            phi_n = totient(n)
            neg_q = not (aut_order == phi_n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: The order of the automorphism group of G is not equal to Euler's totient function phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1