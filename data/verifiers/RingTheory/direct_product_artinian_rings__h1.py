import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import FF

# Standard algebra objects (groups included for completeness, though domains ZZ/QQ are primarily expected)
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
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

def is_artinian(R):
    """
    Helper function to determine if a given ring (represented as a SymPy domain or string) is Artinian.
    """
    if isinstance(R, str):
        R_str = R.strip().replace(' ', '')
        if R_str in ['QQ', 'RR', 'CC', 'Q', 'R', 'C']:
            return True
        if R_str in ['ZZ', 'Z']:
            return False
        if R_str.startswith('FF') or R_str.startswith('F_'):
            return True
        if '[x]' in R_str or '[t]' in R_str:
            return False
        if 'Z/' in R_str or 'Z_n' in R_str:
            return True
            
    if getattr(R, 'is_Field', False):
        return True
    if R == ZZ:
        return False
    if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
        return False
    if hasattr(R, 'is_FractionField') and R.is_FractionField:
        return True
        
    raise ValueError(f"Cannot determine if {R} is Artinian")

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (R_1, R_2), checks if it satisfies the remaining hypothesis
    and falsifies the conclusion.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]
        
    # H_1: R_2 is an Artinian ring
    try:
        h1 = bool(is_artinian(R2))
    except Exception:
        h1 = False
        
    # ¬Q: R_1 x R_2 is NOT an Artinian ring
    # The direct product of two rings is Artinian if and only if both rings are Artinian.
    try:
        art1 = is_artinian(R1)
        art2 = is_artinian(R2)
        prod_artinian = art1 and art2
        neg_q = not prod_artinian
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R_2 is an Artinian ring",
    "¬Q: R_1 x R_2 is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1