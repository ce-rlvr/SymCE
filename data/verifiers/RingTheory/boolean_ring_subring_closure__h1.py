import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = witness
            S = witness
    except Exception:
        return [False, False]

    def contains(domain, item):
        try:
            if item in domain:
                return True
        except Exception:
            pass
        try:
            for x in domain:
                try:
                    if x == item: return True
                    if hasattr(x, 'equals') and x.equals(item): return True
                except Exception:
                    pass
        except TypeError:
            pass
        return False

    h1_ok = False
    try:
        is_R_ring = False
        if R in (ZZ, QQ, RR, CC):
            is_R_ring = True
        elif hasattr(R, 'is_Ring') and R.is_Ring:
            is_R_ring = True
        elif hasattr(R, 'is_ring') and R.is_ring:
            is_R_ring = True
        else:
            try:
                iter(R)
                is_R_ring = True
                if not R:
                    is_R_ring = False
                else:
                    for x in R:
                        for y in R:
                            try:
                                diff = x - y
                                prod = x * y
                            except Exception:
                                is_R_ring = False
                                break
                            if not contains(R, diff):
                                is_R_ring = False
                                break
                            if not contains(R, prod):
                                is_R_ring = False
                                break
                        if not is_R_ring:
                            break
            except TypeError:
                is_R_ring = False

        is_S_subring = False
        if S in (ZZ, QQ, RR, CC) or (hasattr(S, 'is_ring') and S.is_ring) or (hasattr(S, 'is_Ring') and S.is_Ring):
            if S == R:
                is_S_subring = True
            elif S == ZZ and R in (QQ, RR, CC):
                is_S_subring = True
            elif S == QQ and R in (RR, CC):
                is_S_subring = True
            elif S == RR and R == CC:
                is_S_subring = True
            else:
                is_S_subring = False
        else:
            try:
                iter(S)
                is_S_subring = True
                if not S:
                    is_S_subring = False
                else:
                    for x in S:
                        if not contains(R, x):
                            is_S_subring = False
                            break
                    if is_S_subring:
                        for x in S:
                            for y in S:
                                try:
                                    diff = x - y
                                    prod = x * y
                                except Exception:
                                    is_S_subring = False
                                    break
                                if not contains(S, diff):
                                    is_S_subring = False
                                    break
                                if not contains(S, prod):
                                    is_S_subring = False
                                    break
                            if not is_S_subring:
                                break
            except TypeError:
                is_S_subring = False

        h1_ok = is_R_ring and is_S_subring
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if S in (ZZ, QQ, RR, CC):
            neg_q_ok = True
        elif (hasattr(S, 'is_ring') and S.is_ring) or (hasattr(S, 'is_Ring') and S.is_Ring):
            if str(S) == 'GF(2)':
                neg_q_ok = False
            else:
                neg_q_ok = True
        else:
            try:
                iter(S)
                is_boolean = True
                for x in S:
                    try:
                        prod = x * x
                    except Exception:
                        is_boolean = False
                        break
                    if not contains([x], prod):
                        is_boolean = False
                        break
                neg_q_ok = not is_boolean
            except TypeError:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: S is a subring of R",
    "¬Q: S is not a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1