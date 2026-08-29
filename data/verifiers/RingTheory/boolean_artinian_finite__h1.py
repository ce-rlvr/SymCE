import sympy
from sympy import QQ, ZZ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture:
    "An Artinian ring is a finite ring."
    
    H_1: R is an Artinian ring
    neg_Q: R is not a finite ring
    """
    try:
        h1 = False
        name = type(witness).__name__
        
        # Fields are Artinian rings (they have only two ideals, so they satisfy DCC)
        if getattr(witness, 'is_Field', False) or 'Field' in name or witness in [QQ, RR, CC]:
            h1 = True
        elif witness in [sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        # The integers and polynomial rings are not Artinian
        elif witness == ZZ or 'IntegerRing' in name or witness == sympy.S.Integers:
            h1 = False
        elif 'PolynomialRing' in name:
            h1 = False
        else:
            # Any finite ring is Artinian
            is_fin = False
            if 'FiniteField' in name or 'IntegerModRing' in name:
                is_fin = True
            elif hasattr(witness, 'is_finite'):
                is_fin = bool(witness.is_finite)
            if is_fin:
                h1 = True
    except Exception:
        h1 = False

    try:
        is_fin = False
        name = type(witness).__name__
        
        if 'FiniteField' in name or 'IntegerModRing' in name:
            is_fin = True
        elif witness in [ZZ, QQ, RR, CC, sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            is_fin = False
        elif 'RationalField' in name or 'RealField' in name or 'ComplexField' in name or 'IntegerRing' in name or 'PolynomialRing' in name or 'FractionField' in name:
            is_fin = False
        elif hasattr(witness, 'is_finite') and witness.is_finite is not None:
            is_fin = bool(witness.is_finite)
            
        neg_q = not is_fin
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1