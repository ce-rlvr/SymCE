import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_finitely_generated(obj):
    if obj is None:
        raise ValueError("Object is None")
        
    if isinstance(obj, bool):
        return obj
        
    if hasattr(obj, 'is_finitely_generated'):
        val = obj.is_finitely_generated
        return val() if callable(val) else bool(val)
        
    if hasattr(obj, 'generators') or hasattr(obj, 'gens'):
        return True
        
    if obj == sympy.S.Integers:
        return True
    if obj in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
        return False
        
    if hasattr(obj, 'is_finite') and obj.is_finite:
        return True
    if isinstance(obj, (set, list, tuple, frozenset)):
        return True
        
    if isinstance(obj, str):
        obj_lower = obj.lower()
        if obj_lower in ['z', 'integers', 'finite', 'fg', 'finitely generated', 's3', 'z2']:
            return True
        if obj_lower in ['q', 'rationals', 'r', 'reals', 'c', 'complexes', 'infinite', 'not fg', 'not finitely generated']:
            return False
            
    raise ValueError(f"Cannot determine if {obj} is finitely generated")

def conditions(witness) -> list[bool]:
    """
    witness should be a dictionary with keys 'N', 'H', 'G'.
    The values should be objects that can be checked for finite generation,
    or simply booleans indicating whether they are finitely generated.
    For example: {'N': True, 'H': True, 'G': False}
    """
    try:
        if isinstance(witness, dict):
            N = witness.get('N')
            H = witness.get('H')
            G = witness.get('G')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            N, H, G = witness
        elif hasattr(witness, 'N') and hasattr(witness, 'H') and hasattr(witness, 'G'):
            N = witness.N
            H = witness.H
            G = witness.G
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = is_finitely_generated(N)
    except Exception:
        h1 = False

    try:
        h2 = is_finitely_generated(H)
    except Exception:
        h2 = False

    try:
        neg_q = not is_finitely_generated(G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is finitely generated",
    "H_2: H is finitely generated",
    "¬Q: G is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2