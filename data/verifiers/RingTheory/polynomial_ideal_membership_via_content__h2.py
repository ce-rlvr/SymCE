import math
from functools import reduce
from sympy import Poly, abc, S

x = abc.x
ZZ = S.Integers

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            I = witness.get('I')
            f = witness.get('f')
        elif len(witness) == 2:
            I, f = witness
        elif len(witness) == 3:
            _, I, f = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    h1_ok = True

    try:
        p = Poly(f, x)
        coeffs = p.all_coeffs()
        h2_ok = all(c.is_integer for c in coeffs)
    except Exception:
        h2_ok = False

    try:
        def I_contains(I_obj, val):
            if callable(I_obj):
                return bool(I_obj(val))
            try:
                return bool(I_obj.contains(val))
            except AttributeError:
                pass
            return bool(val in I_obj)

        f_in_Ix = all(I_contains(I, int(c)) for c in coeffs)

        g = reduce(math.gcd, [abs(int(c)) for c in coeffs], 0)
        
        if g == 0:
            cf_in_I = I_contains(I, 0)
        else:
            try:
                _ = len(I)
                cf_in_I = False
            except Exception:
                cf_in_I = True
                for k in range(-100, 101):
                    if not I_contains(I, g * k):
                        cf_in_I = False
                        break
        
        equiv = (f_in_Ix == cf_in_I)
        neg_q_ok = not equiv
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a polynomial over R",
    "¬Q: The equivalence fails"
]

N_HYP = 2
NEG_Q_INDEX = 2