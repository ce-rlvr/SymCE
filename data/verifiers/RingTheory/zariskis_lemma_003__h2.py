import math
import sympy
from sympy import QQ, ZZ, RR, CC
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        k, E = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = getattr(k, 'is_Field', False)
        if callable(h1):
            h1 = h1()
        h1_ok = bool(h1)
    except Exception:
        h1_ok = False

    try:
        h2 = getattr(E, 'is_Field', False)
        if callable(h2):
            h2 = h2()
        h2_ok = bool(h2)
    except Exception:
        h2_ok = False

    try:
        def is_finite_algebraic_extension(E, k):
            if E == k:
                return True
            
            try:
                if type(E).__name__ == 'AlgebraicField':
                    if E.domain == k:
                        return True
                    if is_finite_algebraic_extension(E.domain, k):
                        return True
                    if is_finite_algebraic_extension(E, E.domain) and is_finite_algebraic_extension(k, E.domain):
                        if hasattr(k, 'unify') and k.unify(E) == E:
                            return True
            except Exception:
                pass

            try:
                if type(E).__name__ == 'ComplexField' and type(k).__name__ == 'RealField':
                    return True
            except Exception:
                pass

            try:
                if getattr(E, 'is_FiniteField', False) and getattr(k, 'is_FiniteField', False):
                    p_E = E.characteristic() if callable(getattr(E, 'characteristic', None)) else E.characteristic
                    p_k = k.characteristic() if callable(getattr(k, 'characteristic', None)) else k.characteristic
                    if p_E == p_k:
                        p = int(p_E)
                        order_E = int(E.order() if callable(getattr(E, 'order', None)) else E.order)
                        order_k = int(k.order() if callable(getattr(k, 'order', None)) else k.order)
                        n = round(math.log(order_E, p))
                        m = round(math.log(order_k, p))
                        if n % m == 0:
                            return True
            except Exception:
                pass

            return False

        neg_q_ok = not is_finite_algebraic_extension(E, k)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: E is a field",
    "¬Q: E is not a finite algebraic extension of k"
]

N_HYP = 2
NEG_Q_INDEX = 2