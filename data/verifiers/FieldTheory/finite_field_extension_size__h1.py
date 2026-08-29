import sympy
from sympy import I, sqrt
from sympy.polys.domains import QQ, RR, CC, ZZ

Q_sqrt2 = QQ.algebraic_field(sqrt(2))
Q_I = QQ.algebraic_field(I)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            K, F, n, q = witness
        elif len(witness) == 3:
            K, F, n = witness
            q = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_extension(K, F):
        if not getattr(K, 'is_Field', False): return False
        if not getattr(F, 'is_Field', False): return False
        if F == QQ:
            if K == QQ: return True
            if hasattr(K, 'domain') and K.domain == QQ: return True
        if F == RR:
            if K in (RR, CC): return True
        if F == CC:
            if K == CC: return True
        if getattr(F, 'is_FiniteField', False):
            if K == F: return True
        return False

    def get_degree(K, F):
        if F == QQ:
            if K == QQ: return 1
            if hasattr(K, 'domain') and K.domain == QQ:
                if hasattr(K, 'mod'): return K.mod.degree()
        if F == RR:
            if K == RR: return 1
            if K == CC: return 2
        if F == CC:
            if K == CC: return 1
        if getattr(F, 'is_FiniteField', False):
            if K == F: return 1
        return None

    try:
        h1 = is_extension(K, F)
    except Exception:
        h1 = False

    try:
        deg = get_degree(K, F)
        is_int = isinstance(n, int) or getattr(n, 'is_integer', False)
        h2 = (deg is not None) and (deg == n) and is_int
    except Exception:
        h2 = False

    try:
        is_finite = getattr(K, 'is_FiniteField', False)
        if not is_finite and hasattr(K, 'order'):
            try:
                o = K.order() if callable(K.order) else K.order
                if isinstance(o, (int, sympy.Integer)):
                    is_finite = True
            except Exception:
                pass

        if not is_finite:
            neg_q = True
        else:
            if q is not None:
                size = K.order() if callable(K.order) else K.order
                neg_q = (size != q**n)
            else:
                if hasattr(F, 'order'):
                    f_size = F.order() if callable(F.order) else F.order
                    size = K.order() if callable(K.order) else K.order
                    neg_q = (size != f_size**n)
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: K is a field extension of F", "H_2: The degree of the extension K over F is a finite integer n", "¬Q: K is not a finite field containing exactly q^n elements"]
N_HYP = 2
NEG_Q_INDEX = 2