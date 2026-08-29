import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.agca.modules import Module

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
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_R_module', False))
            is_noeth = bool(witness.get('is_noetherian', False))
            every_fg = bool(witness.get('every_submodule_finitely_generated', False))
            neg_q = is_noeth != every_fg
        elif isinstance(witness, tuple) and len(witness) == 3:
            h1 = bool(witness[0])
            is_noeth = bool(witness[1])
            every_fg = bool(witness[2])
            neg_q = is_noeth != every_fg
        elif isinstance(witness, Module):
            h1 = True
            # SymPy modules in agca are over polynomial rings over fields, 
            # which are Noetherian, so every submodule is finitely generated.
            is_noeth = True
            every_fg = True
            neg_q = is_noeth != every_fg
        else:
            h1 = bool(getattr(witness, 'is_R_module', False))
            is_noeth = bool(getattr(witness, 'is_noetherian', False))
            every_fg = bool(getattr(witness, 'every_submodule_finitely_generated', False))
            neg_q = is_noeth != every_fg
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "¬Q: It is FALSE that M is a Noetherian module if and only if every submodule of M is finitely generated"
]

N_HYP = 1
NEG_Q_INDEX = 1