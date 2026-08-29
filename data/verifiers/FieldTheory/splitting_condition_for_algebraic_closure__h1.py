import sympy
from sympy import QQ, RR, CC, I
from sympy.polys.domains.algebraicfield import AlgebraicField
from sympy.abc import x

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: E is an extension field of F",
    "H_2: E is an algebraic extension of F",
    "H_3: Every non-constant polynomial over F splits completely into linear factors over E",
    "¬Q: E is not an algebraically closed field"
]

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('H1', False))
            h2 = bool(witness.get('H2', False))
            h3 = bool(witness.get('H3', False))
            neg_q = bool(witness.get('neg_Q', False))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    if hasattr(witness, 'H1'):
        try:
            h1 = bool(witness.H1)
            h2 = bool(witness.H2)
            h3 = bool(witness.H3)
            neg_q = bool(witness.neg_Q)
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, E = witness
            
            if F == RR and E == CC:
                return [True, True, True, False]
            if F == QQ and E == CC:
                return [True, False, True, False]
            if F == QQ and E == QQ:
                return [True, True, False, True]
            if F == RR and E == RR:
                return [True, True, False, True]
            if F == CC and E == CC:
                return [True, True, True, False]
                
            if F == QQ and isinstance(E, AlgebraicField):
                return [True, True, False, True]
                
            if F.__class__.__name__ == 'FiniteField' and E.__class__.__name__ == 'FiniteField':
                if F.characteristic == E.characteristic:
                    return [True, True, False, True]
    except Exception:
        pass

    return [h1, h2, h3, neg_q]