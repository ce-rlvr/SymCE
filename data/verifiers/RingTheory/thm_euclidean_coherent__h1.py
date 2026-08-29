import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

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

def is_coherent(witness):
    # If the witness explicitly declares whether it is coherent
    if hasattr(witness, 'is_coherent'):
        return bool(witness.is_coherent)
        
    # If the witness is provided as a string description
    if isinstance(witness, str):
        s = witness.lower().strip()
        non_coherent_keywords = [
            '...', 'infinite', 'oo', 'continuous', 
            '^n', '^{n}', '^\\mathbb{n}', '\\prod', 'direct product',
            'z^n', 'z^\\mathbb{n}', 'non-coherent', 'not coherent'
        ]
        for kw in non_coherent_keywords:
            if kw in s:
                return False
        # Otherwise, assume it describes a standard coherent ring (e.g., Z, Q[x], etc.)
        return True

    # All implemented SymPy domains (ZZ, QQ, PolyRing, FracField, etc.) are Noetherian, hence coherent
    try:
        from sympy.polys.domains.domain import Domain
        if isinstance(witness, Domain):
            return True
    except Exception:
        pass
        
    # Standard SymPy sets representing coherent rings
    try:
        from sympy import S
        if witness in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            return True
    except Exception:
        pass

    # Groups are not rings
    try:
        from sympy.combinatorics.groups import PermutationGroup
        if isinstance(witness, PermutationGroup):
            return False
    except Exception:
        pass
        
    # Matrices are elements, not rings
    try:
        from sympy.matrices.matrices import MatrixBase
        if isinstance(witness, MatrixBase):
            return False
    except Exception:
        pass

    # Other SymPy expressions (like symbols, polynomials, etc.) are elements, not rings
    try:
        from sympy.core.basic import Basic
        if isinstance(witness, Basic):
            return False
    except Exception:
        pass

    # Basic Python types are not rings
    if isinstance(witness, (int, float, bool, list, tuple, dict, set)):
        return False

    # Default to True to avoid false positives in the verifier
    return True

def conditions(witness) -> list[bool]:
    try:
        # The conclusion is "R is a coherent ring".
        # We want neg_Q to be True when the conclusion FAILS (i.e., R is NOT a coherent ring).
        neg_q = not is_coherent(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a coherent ring"
]

N_HYP = 0
NEG_Q_INDEX = 0