import sympy
import math

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "H_2: n and m are coprime",
    "H_3: ζ_n is a primitive n-th root of unity",
    "¬Q: The intersection of the fields ℚ(ζ_n) ∩ ℚ(ζ_m) is not ℚ"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        n, m, zeta_n, zeta_m = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(n, int) and n > 0 and isinstance(m, int) and m > 0
    except Exception:
        h1 = False

    try:
        h2 = math.gcd(n, m) == 1
    except Exception:
        h2 = False

    try:
        is_root = sympy.simplify(zeta_n**n - 1) == 0
        is_prim = True
        for k in range(1, n):
            if sympy.simplify(zeta_n**k - 1) == 0:
                is_prim = False
                break
        h3 = bool(is_root and is_prim)
    except Exception:
        h3 = False

    try:
        is_not_rational = True
        try:
            sympy.Rational(sympy.simplify(zeta_m))
            is_not_rational = False
        except TypeError:
            pass
        except Exception:
            pass

        in_field = False
        for i in range(1, n):
            if sympy.simplify(zeta_m - zeta_n**i) == 0:
                in_field = True
                break
            if sympy.simplify(zeta_m + zeta_n**i) == 0:
                in_field = True
                break
                
        neg_q = bool(is_not_rational and in_field)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]