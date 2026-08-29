import sympy
from sympy.polys.domains import QQ, ZZ, RR, CC, GF, EX
from sympy import Symbol, sqrt, I

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def is_perfect_field(F):
    if not getattr(F, 'is_Field', False):
        return False
    char_func = getattr(F, 'characteristic', None)
    char = char_func() if callable(char_func) else char_func
    if char == 0:
        return True
    if char is not None and char > 0:
        name = F.__class__.__name__
        if getattr(F, 'is_FiniteField', False) or 'FiniteField' in name or 'GaloisField' in name or 'GF' in name:
            return True
        if name == 'AlgebraicField' and is_perfect_field(F.domain):
            return True
    return False

def is_extension(E, F):
    if not getattr(E, 'is_Field', False):
        return False
    if not getattr(F, 'is_Field', False):
        return False
    
    char_E = getattr(E, 'characteristic', lambda: None)() if callable(getattr(E, 'characteristic', None)) else getattr(E, 'characteristic', None)
    char_F = getattr(F, 'characteristic', lambda: None)() if callable(getattr(F, 'characteristic', None)) else getattr(F, 'characteristic', None)
    
    if char_E != char_F:
        return False

    if E == F:
        return True
    if hasattr(E, 'domain') and E.domain == F:
        return True
    try:
        if E.convert(F.one) == E.one:
            return True
    except Exception:
        pass
    return False

def is_alg(dom, base):
    if dom == base:
        return True
    name = dom.__class__.__name__
    if name == 'AlgebraicField':
        return is_alg(dom.domain, base)
    if name == 'ComplexField' and base.__class__.__name__ == 'RealField':
        return True
    if name in ('FractionField', 'ExpressionDomain', 'RealField', 'ComplexField'):
        return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        F, E = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(is_perfect_field(F))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_extension(E, F))
    except Exception:
        h2 = False

    try:
        neg_q = not bool(is_alg(E, F))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "H_2: E is a field extension of F",
    "¬Q: The field extension E/F is not separable"
]

N_HYP = 2
NEG_Q_INDEX = 2