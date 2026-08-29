import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    Since SymPy does not have a comprehensive commutative algebra module for 
    localization of arbitrary modules, this verifier expects a mock witness 
    (dictionary or object) that explicitly provides the required properties.
    """
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('M_is_finitely_generated', False))
            h2 = bool(witness.get('S_is_multiplicatively_closed', False))
            if 'S_inv_M_is_finitely_generated' in witness:
                neg_q = not bool(witness['S_inv_M_is_finitely_generated'])
        else:
            h1 = bool(getattr(witness, 'M_is_finitely_generated', False))
            h2 = bool(getattr(witness, 'S_is_multiplicatively_closed', False))
            if hasattr(witness, 'S_inv_M_is_finitely_generated'):
                neg_q = not bool(getattr(witness, 'S_inv_M_is_finitely_generated'))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}M is not a finitely generated S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2