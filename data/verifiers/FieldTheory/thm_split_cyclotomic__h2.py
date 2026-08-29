import sympy
from sympy.ntheory import totient
from sympy.abc import x

# Top-level setup for named objects that a witness expression might reference
ZZ = sympy.ZZ
QQ = sympy.QQ
GF = sympy.GF

def conditions(witness):
    """
    Given a witness object, evaluates the remaining hypotheses and the negated conclusion.
    The witness is expected to be a tuple (n, F, K) or an object with these attributes,
    where F is a base ring/field (e.g., ZZ, QQ, GF(p)) and K is the splitting field.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            n, F, K = witness
        else:
            n = witness.n
            F = witness.F
            K = witness.K
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # H_2: The characteristic of F does not divide n
    try:
        char = F.characteristic()
        h2 = (char == 0) or (n % char != 0)
    except Exception:
        h2 = False

    # H_3: K is the splitting field of x^n - 1 over F
    try:
        char = F.characteristic()
        if char > 0:
            p = char
            if n % p == 0:
                h3 = False
            else:
                # For finite fields, the splitting field of x^n - 1 over GF(p) is GF(p^d)
                # where d is the multiplicative order of p modulo n.
                d = 1
                while (p**d) % n != 1:
                    d += 1
                if hasattr(K, 'order'):
                    h3 = (K.order == p**d)
                else:
                    h3 = False
        else:
            # For characteristic 0, we check standard domains ZZ and QQ.
            # The splitting field over ZZ or QQ is the n-th cyclotomic field,
            # which has degree totient(n) over QQ.
            if F in (ZZ, QQ):
                if not getattr(K, 'is_Field', False):
                    h3 = False
                else:
                    if K == QQ:
                        deg = 1
                    else:
                        deg = None
                        for attr in ('degree', 'ext'):
                            if hasattr(K, attr):
                                val = getattr(K, attr)
                                if callable(val):
                                    deg = val()
                                elif hasattr(val, 'degree'):
                                    deg = val.degree()
                                    if callable(deg):
                                        deg = deg()
                                else:
                                    deg = val
                                break
                        if deg is None:
                            deg = 1
                    h3 = (deg == totient(n))
            else:
                h3 = False
    except Exception:
        h3 = False

    # ¬Q: K != F(\zeta), where \zeta is a primitive n-th root of unity in K
    # The dropped hypothesis from the true theorem is "F is a field".
    # If F is a field, K = F(\zeta) is mathematically guaranteed to be true.
    # If F is an integral domain (like ZZ), F(\zeta) is a ring (e.g., ZZ[\zeta]), 
    # which is not a field and therefore cannot equal the splitting field K.
    try:
        is_field = getattr(F, 'is_Field', False)
        neg_q = not is_field
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: The characteristic of F does not divide n",
    "H_3: K is the splitting field of x^n - 1 over F",
    "¬Q: K != F(\\zeta), where \\zeta is a primitive n-th root of unity in K"
]

N_HYP = 3
NEG_Q_INDEX = 3