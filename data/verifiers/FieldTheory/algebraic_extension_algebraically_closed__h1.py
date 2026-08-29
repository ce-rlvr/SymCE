import sympy
from sympy import I, sqrt, Rational, Poly, Symbol
from sympy.polys.domains import QQ, RR, CC, ZZ, FF, GF
import math

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        L, K = witness
    except Exception:
        return [False, False]
        
    # H1: L is an algebraic field extension of K
    h1 = False
    try:
        if L == K:
            if getattr(L, 'is_Field', False) or type(L).__name__ in (
                'RationalField', 'RealField', 'ComplexField', 
                'AlgebraicField', 'FiniteField', 'GaloisField'
            ):
                h1 = True
        elif getattr(L, 'is_AlgebraicField', False) and getattr(L, 'domain', None) == K:
            h1 = True
        elif type(L).__name__ == 'AlgebraicField' and getattr(L, 'domain', None) == K:
            h1 = True
        elif L == CC and K == RR:
            h1 = True
        elif hasattr(L, 'order') and hasattr(K, 'order') and hasattr(L, 'characteristic') and hasattr(K, 'characteristic'):
            char_L = L.characteristic() if callable(L.characteristic) else L.characteristic
            char_K = K.characteristic() if callable(K.characteristic) else K.characteristic
            if char_L == char_K and char_L > 0:
                p1 = L.order
                p2 = K.order
                if p1 >= p2:
                    log_val = math.log(p1, p2)
                    if abs(log_val - round(log_val)) < 1e-9:
                        h1 = True
        elif getattr(L, 'is_Poly', False) or isinstance(L, Poly):
            if getattr(L, 'domain', None) == K and getattr(L, 'is_irreducible', False):
                h1 = True
    except Exception:
        pass

    # neg_Q: L != K or the extension degree is not 1
    neg_q = False
    try:
        if getattr(L, 'is_Poly', False) or isinstance(L, Poly):
            if L.degree() > 1:
                neg_q = True
        elif L != K:
            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: L is an algebraic field extension of K", "¬Q: L is not K or the extension degree is not 1"]

N_HYP = 1
NEG_Q_INDEX = 1