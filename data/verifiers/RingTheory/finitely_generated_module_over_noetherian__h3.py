import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

# Top-level setup for witness construction
# Standard rings and fields
Z = ZZ
Q = QQ
R = RR
C = CC

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is an R-module",
    "¬Q: M is not a Noetherian module (does not satisfy ACC on submodules)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        R_ring, M_mod = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative Noetherian ring
    try:
        h1 = False
        # All standard SymPy domains are commutative Noetherian rings
        # (fields, ZZ, and polynomial rings over them in finitely many variables)
        if hasattr(R_ring, 'unify') and hasattr(R_ring, 'is_Field'):
            h1 = True
    except Exception:
        h1 = False
        
    # H2: M is an R-module
    try:
        h2 = False
        # M is an R-module (algebra) if R can be unified into M without changing M
        if hasattr(M_mod, 'unify') and hasattr(R_ring, 'unify'):
            if M_mod.unify(R_ring) == M_mod:
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: M is NOT a Noetherian R-module
    try:
        is_noeth = True
        if R_ring == M_mod:
            is_noeth = True
        elif R_ring == ZZ and M_mod in (QQ, RR, CC):
            is_noeth = False
        elif R_ring == QQ and M_mod in (RR, CC):
            is_noeth = False
        elif type(M_mod).__name__ == 'FiniteField' or getattr(M_mod, 'is_FiniteField', False):
            is_noeth = True
        elif hasattr(M_mod, 'is_AlgebraicField') and M_mod.is_AlgebraicField:
            if R_ring == ZZ:
                is_noeth = False
            elif getattr(R_ring, 'is_Field', False):
                is_noeth = True
        elif hasattr(M_mod, 'gens') and len(M_mod.gens) > 0:
            # Polynomial or fraction field over some base
            # Since R_ring != M_mod, it is not finitely generated over R_ring
            is_noeth = False
        elif hasattr(M_mod, 'is_Field') and M_mod.is_Field and not getattr(R_ring, 'is_Field', False):
            # M is a field, R is not a field (e.g. M=QQ, R=ZZ)
            is_noeth = False
            
        neg_q = not is_noeth
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]