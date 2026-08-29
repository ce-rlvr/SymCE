import sympy
from sympy import S
from sympy.polys.domains import QQ, RR, CC, ZZ, FF

Rationals = S.Rationals
Reals = S.Reals
Complexes = S.Complexes
Integers = S.Integers
Naturals = S.Naturals

def is_field(x):
    if x in (S.Rationals, S.Reals, S.Complexes):
        return True
    if hasattr(x, 'is_Field') and x.is_Field:
        return True
    if hasattr(x, 'is_field') and x.is_field:
        return True
    return False

def is_countable(x):
    if hasattr(x, 'is_countable') and x.is_countable is True:
        return True
    if x in (S.Rationals, S.Integers, S.Naturals, S.Naturals0):
        return True
    if hasattr(x, 'is_RationalField') and x.is_RationalField:
        return True
    if hasattr(x, 'is_FiniteField') and x.is_FiniteField:
        return True
    if hasattr(x, 'is_IntegerRing') and x.is_IntegerRing:
        return True
    return False

def is_uncountable(x):
    if hasattr(x, 'is_countable') and x.is_countable is False:
        return True
    if x in (S.Reals, S.Complexes):
        return True
    if hasattr(x, 'is_RealField') and x.is_RealField:
        return True
    if hasattr(x, 'is_ComplexField') and x.is_ComplexField:
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            K = witness.get('K')
        else:
            F, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = bool(is_field(F))
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(is_countable(F))
    except Exception:
        h2_ok = False
        
    try:
        neg_q_ok = bool(is_uncountable(K))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F is a countable set",
    "¬Q: K is not a countable set"
]

N_HYP = 2
NEG_Q_INDEX = 2