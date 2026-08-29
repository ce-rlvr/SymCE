import sympy
from sympy import S
from sympy.polys.domains import ZZ as poly_ZZ, QQ as poly_QQ, RR as poly_RR, CC as poly_CC

# Top-level setup: named object bindings that the witness expression may reference
ZZ = S.Integers
QQ = S.Rationals
RR = S.Reals
CC = S.Complexes

def conditions(witness) -> list[bool]:
    def has_at_least_two_elements(w):
        if w in (ZZ, QQ, RR, CC, poly_ZZ, poly_QQ, poly_RR, poly_CC):
            return True
        if hasattr(w, 'is_infinite'):
            is_inf = w.is_infinite() if callable(w.is_infinite) else w.is_infinite
            if is_inf:
                return True
        if hasattr(w, 'size'):
            size = w.size() if callable(w.size) else w.size
            if size >= 2:
                return True
        if hasattr(w, 'order'):
            order = w.order() if callable(w.order) else w.order
            if order >= 2:
                return True
        if hasattr(w, '__len__'):
            try:
                if len(w) >= 2:
                    return True
            except Exception:
                pass
        if hasattr(w, 'domain') and w.domain is not w:
            return has_at_least_two_elements(w.domain)
        return False

    try:
        h1 = bool(has_at_least_two_elements(witness))
    except Exception:
        h1 = False

    def is_ordered_ring(w):
        if w in (ZZ, QQ, RR, poly_ZZ, poly_QQ, poly_RR):
            return True
        if hasattr(w, 'is_subset'):
            try:
                if w.is_subset(RR):
                    return True
            except Exception:
                pass
        if hasattr(w, 'domain') and w.domain is not w:
            return is_ordered_ring(w.domain)
        return False

    try:
        neg_q = bool(is_ordered_ring(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R has at least two distinct elements",
    "¬Q: There exists a total order on R that makes R an ordered ring"
]

N_HYP = 1
NEG_Q_INDEX = 1