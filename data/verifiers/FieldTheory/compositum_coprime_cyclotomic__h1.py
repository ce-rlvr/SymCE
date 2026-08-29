import sympy
import math
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: n and m are coprime",
    "H_2: ζ_n is a primitive n-th root of unity",
    "H_3: ζ_m is a primitive m-th root of unity",
    "¬Q: The compositum field ℚ(ζ_n)ℚ(ζ_m) is not equal to ℚ(ζ_{nm})"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_primitive_root(val_z, k):
    try:
        if not isinstance(k, int) or k < 1:
            return False
        
        try:
            c_val = complex(val_z)
            if abs(c_val**k - 1) > 1e-7:
                return False
            for d in sympy.divisors(k):
                if d < k:
                    if abs(c_val**d - 1) < 1e-7:
                        return False
            return True
        except Exception:
            pass
        
        if sympy.simplify(val_z**k - 1) != 0:
            return False
        for d in sympy.divisors(k):
            if d < k:
                if sympy.simplify(val_z**d - 1) == 0:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, m = witness
                check_roots = False
            elif len(witness) >= 5:
                n, m, z_n, z_m, z_nm = witness[:5]
                check_roots = True
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        n = int(n)
        m = int(m)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = (math.gcd(n, m) == 1)
    except Exception:
        h1 = False

    try:
        if check_roots:
            h2 = is_primitive_root(z_n, n)
        else:
            h2 = (n >= 1)
    except Exception:
        h2 = False

    try:
        if check_roots:
            h3 = is_primitive_root(z_m, m)
        else:
            h3 = (m >= 1)
    except Exception:
        h3 = False

    try:
        if n >= 1 and m >= 1:
            lcm_nm = (n * m) // math.gcd(n, m)
            deg_compositum = sympy.totient(lcm_nm)
            deg_nm = sympy.totient(n * m)
            neg_q = bool(deg_compositum != deg_nm)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]