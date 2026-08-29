import sympy
from sympy import QQ, RR, CC, ZZ, S
from sympy.polys.domains import FiniteField, RationalField, RealField, ComplexField, AlgebraicField, FractionField

def get_cardinality(F):
    if F in (QQ, S.Rationals): return 'aleph_0'
    if F in (RR, S.Reals): return 'continuum'
    if F in (CC, S.Complexes): return 'continuum'
    if F in (ZZ, S.Integers): return 'aleph_0'
    
    if hasattr(F, 'is_FiniteField') and F.is_FiniteField:
        return F.order
    if hasattr(F, 'order'):
        try:
            return int(F.order)
        except Exception:
            pass
    if isinstance(F, FiniteField):
        return F.order
    if isinstance(F, (RationalField, AlgebraicField)):
        return 'aleph_0'
    if isinstance(F, FractionField):
        if F.domain in (RR, CC, S.Reals, S.Complexes):
            return 'continuum'
        return 'aleph_0'
    if isinstance(F, (RealField, ComplexField)):
        return 'continuum'
    
    s = str(F)
    if s in ['QQ', 'ZZ', 'Rationals', 'Integers']: return 'aleph_0'
    if s in ['RR', 'CC', 'Reals', 'Complexes']: return 'continuum'
    
    return None

def conditions(witness) -> list[bool]:
    # H_1: F is a field
    try:
        if isinstance(witness, str):
            if witness in ['QQ', 'RR', 'CC', 'Rationals', 'Reals', 'Complexes']:
                h1 = True
            elif witness in ['ZZ', 'Integers']:
                h1 = False
            else:
                h1 = False
        elif witness in (S.Rationals, S.Reals, S.Complexes, QQ, RR, CC):
            h1 = True
        elif witness in (S.Integers, ZZ):
            h1 = False
        elif hasattr(witness, 'is_Field'):
            h1 = bool(witness.is_Field)
        elif hasattr(witness, 'is_field'):
            h1 = bool(witness.is_field)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: F is an infinite field
    try:
        c = get_cardinality(witness)
        if c in ['aleph_0', 'continuum']:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The cardinality of the algebraic closure of F is NOT equal to the cardinality of F
    try:
        cF = get_cardinality(witness)
        if cF is None:
            neg_q = False
        else:
            if isinstance(cF, int):
                c_alg = 'aleph_0'
            else:
                c_alg = cF
            neg_q = bool(cF != c_alg)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F is an infinite field",
    "¬Q: The cardinality of the algebraic closure of F is not equal to the cardinality of F"
]

N_HYP = 2
NEG_Q_INDEX = 2