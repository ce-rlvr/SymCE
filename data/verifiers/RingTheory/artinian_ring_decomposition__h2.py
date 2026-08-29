import sympy
from sympy import symbols, S
from sympy.polys.domains import ZZ, QQ, RR, CC, FF
from sympy.polys.domains.domain import Domain
from sympy.polys.rings import PolyRing

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    R = witness
    
    # Normalize common SymPy sets to their Domain equivalents
    if R == S.Integers:
        R = ZZ
    elif R == S.Rationals:
        R = QQ
    elif R == S.Reals:
        R = RR
    elif R == S.Complexes:
        R = CC

    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if isinstance(R, Domain) or isinstance(R, PolyRing):
            h1 = True
        elif R.__class__.__name__ in ('QuotientRing', 'GlobalPolynomialRing', 'GeneralizedPolynomialRing'):
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: R is NOT isomorphic to a finite direct product of Artinian local rings
    # For integral domains (which SymPy Domains are), this is equivalent to R NOT being a field.
    try:
        is_artinian = False
        if hasattr(R, 'is_Field') and R.is_Field:
            is_artinian = True
        elif isinstance(R, Domain):
            is_artinian = bool(R.is_Field)
        elif isinstance(R, PolyRing):
            is_artinian = False
        elif R == ZZ:
            is_artinian = False
            
        neg_q = not is_artinian
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: R is not isomorphic to a finite direct product of Artinian local rings"
]

N_HYP = 1
NEG_Q_INDEX = 1