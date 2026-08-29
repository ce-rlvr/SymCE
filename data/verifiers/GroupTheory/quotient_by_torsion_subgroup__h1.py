import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            if 'T_is_torsion_subgroup' in witness:
                h1 = bool(witness['T_is_torsion_subgroup'])
                q = bool(witness.get('G_mod_T_is_torsion_free', True))
                return [h1, not q]
            if 'is_torsion_subgroup' in witness:
                h1 = bool(witness['is_torsion_subgroup'])
                q = bool(witness.get('quotient_is_torsion_free', True))
                return [h1, not q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'T_is_torsion_subgroup'):
            h1 = bool(witness.T_is_torsion_subgroup)
            if hasattr(witness, 'G_mod_T_is_torsion_free'):
                neg_q = not bool(witness.G_mod_T_is_torsion_free)
            elif hasattr(witness, 'quotient_is_torsion_free'):
                neg_q = not bool(witness.quotient_is_torsion_free)
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_torsion_subgroup') and callable(witness.is_torsion_subgroup):
            h1 = bool(witness.is_torsion_subgroup())
            if hasattr(witness, 'quotient_is_torsion_free'):
                neg_q = not bool(witness.quotient_is_torsion_free())
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, T = witness
            if hasattr(G, 'torsion_subgroup') and hasattr(G, 'quotient'):
                h1 = (G.torsion_subgroup() == T)
                neg_q = not G.quotient(T).is_torsion_free()
                return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: T is the torsion subgroup of G",
    "¬Q: The quotient group G/T is not torsion-free"
]

N_HYP = 1
NEG_Q_INDEX = 1