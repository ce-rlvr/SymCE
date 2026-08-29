import sympy
from sympy.combinatorics import FreeGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                F, K, a, b = witness
            elif len(witness) == 2:
                F, K = witness
                a, b = None, None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(F, FreeGroup)
    except Exception:
        h1 = False

    try:
        h2 = bool(getattr(K, 'is_Field', False))
    except Exception:
        h2 = False

    try:
        if a is None or b is None:
            neg_q = False
        else:
            if isinstance(a, list):
                a = dict(a)
            if isinstance(b, list):
                b = dict(b)

            def is_zero(v):
                if v == 0:
                    return True
                if hasattr(K, 'is_zero'):
                    try:
                        if K.is_zero(v):
                            return True
                    except Exception:
                        pass
                if hasattr(K, 'zero'):
                    try:
                        if v == K.zero:
                            return True
                    except Exception:
                        pass
                if hasattr(v, 'is_zero') and v.is_zero:
                    return True
                try:
                    if sympy.expand(v) == 0:
                        return True
                except Exception:
                    pass
                return False

            a_nonzero = any(not is_zero(v) for v in a.values())
            b_nonzero = any(not is_zero(v) for v in b.values())

            if not (a_nonzero and b_nonzero):
                neg_q = False
            else:
                prod = {}
                for g1, c1 in a.items():
                    for g2, c2 in b.items():
                        g = g1 * g2
                        if hasattr(K, 'mul'):
                            try:
                                c = K.mul(c1, c2)
                            except Exception:
                                c = c1 * c2
                        else:
                            c = c1 * c2
                            
                        if g in prod:
                            if hasattr(K, 'add'):
                                try:
                                    prod[g] = K.add(prod[g], c)
                                except Exception:
                                    prod[g] = prod[g] + c
                            else:
                                prod[g] = prod[g] + c
                        else:
                            prod[g] = c

                prod_zero = all(is_zero(v) for v in prod.values())
                neg_q = bool(prod_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: K is a field",
    "¬Q: group ring has non-zero zero divisors"
]

N_HYP = 2
NEG_Q_INDEX = 2