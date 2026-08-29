import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import Domain
from sympy.polys.rings import PolyRing

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
    # Map SymPy sets to domains if provided for convenience
    try:
        if witness is S.Integers:
            witness = ZZ
        elif witness is S.Rationals:
            witness = QQ
        elif witness is S.Reals:
            witness = RR
        elif witness is S.Complexes:
            witness = CC
    except Exception:
        pass

    # H1: R is a commutative ring
    try:
        h1 = isinstance(witness, (Domain, PolyRing))
    except Exception:
        h1 = False
        
    # H2: R has a multiplicative identity
    try:
        h2 = False
        if h1:
            if hasattr(witness, 'one') and witness.one is not None:
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: R is NOT isomorphic to a finite direct product of Artinian local rings
    try:
        neg_q = False
        if h1:
            is_art = True
            w_type = type(witness).__name__
            
            if w_type == 'QuotientRing':
                # Safe fallback: assume quotient rings might be Artinian to avoid false positives
                is_art = True 
            elif w_type == 'PolyRing':
                # Polynomial rings over any ring are never Artinian
                is_art = False 
            elif hasattr(witness, 'is_Field'):
                # For integral domains (which SymPy Domains are), 
                # being Artinian is equivalent to being a field.
                is_art = witness.is_Field
            else:
                is_art = True # Safe fallback
                
            neg_q = not is_art
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "¬Q: R is not isomorphic to a finite direct product of Artinian local rings"
]

N_HYP = 2
NEG_Q_INDEX = 2