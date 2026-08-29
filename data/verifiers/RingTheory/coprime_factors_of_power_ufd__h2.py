import sympy
import math

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')
ZZ = sympy.ZZ
QQ = sympy.QQ

def is_exact_nth_power(val, n):
    if val < 0:
        return False
    if val == 0 or val == 1:
        return True
    low = 1
    high = val
    while low <= high:
        mid = (low + high) // 2
        p = mid ** n
        if p == val:
            return True
        elif p < val:
            low = mid + 1
        else:
            high = mid - 1
    return False

def is_nth_power_up_to_unit(val, n, R):
    try:
        if R == sympy.ZZ or R == sympy.S.Integers:
            val_sym = sympy.sympify(val)
            if not val_sym.is_integer:
                return False
            val_int = abs(int(val_sym))
            return is_exact_nth_power(val_int, int(n))
        elif R == sympy.QQ or R == sympy.S.Rationals:
            return True
        else:
            const, factors = sympy.factor_list(val)
            for base, exp in factors:
                if exp % int(n) != 0:
                    return False
            if hasattr(R, 'domain'):
                base_ring = R.domain
                if base_ring == sympy.ZZ:
                    c = abs(int(const))
                    return is_exact_nth_power(c, int(n))
            return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            n = witness.get('n')
        else:
            R, a, b, c, n = witness
    except Exception:
        return [False] * 5

    # H_1: R is a unique factorization domain
    try:
        if R == sympy.ZZ or R == sympy.S.Integers:
            H1 = True
        elif R == sympy.QQ or R == sympy.S.Rationals:
            H1 = True
        elif hasattr(R, 'is_UFD'):
            H1 = bool(R.is_UFD)
        else:
            H1 = False
    except Exception:
        H1 = False

    # H_2: n is a positive integer
    try:
        n_val = int(n)
        H2 = (n_val > 0 and n_val == n)
    except Exception:
        H2 = False

    # H_3: The greatest common divisor of a and b is a unit
    try:
        if R == sympy.ZZ or R == sympy.S.Integers:
            a_sym = sympy.sympify(a)
            b_sym = sympy.sympify(b)
            if not (a_sym.is_integer and b_sym.is_integer):
                H3 = False
            else:
                g = math.gcd(int(a_sym), int(b_sym))
                H3 = (g == 1)
        elif R == sympy.QQ or R == sympy.S.Rationals:
            H3 = (a != 0 or b != 0)
        else:
            if hasattr(R, 'gcd'):
                g = R.gcd(a, b)
            else:
                g = sympy.gcd(a, b)
                
            if hasattr(R, 'is_unit'):
                H3 = bool(R.is_unit(g))
            elif hasattr(R, 'rem') and hasattr(R, 'one') and hasattr(R, 'zero'):
                H3 = bool(R.rem(R.one, g) == R.zero)
            else:
                g_simp = sympy.simplify(g)
                if g_simp.is_number:
                    if R == sympy.ZZ or R == sympy.S.Integers:
                        H3 = (abs(int(g_simp)) == 1)
                    else:
                        H3 = (g_simp != 0)
                else:
                    H3 = False
    except Exception:
        H3 = False

    # H_4: ab = c^n
    try:
        diff = sympy.simplify(a * b - c ** n)
        if diff == 0:
            H4 = True
        else:
            H4 = (sympy.expand(diff) == 0)
    except Exception:
        H4 = False

    # ¬Q: a and b are not both n-th powers up to a unit in R
    try:
        a_ok = is_nth_power_up_to_unit(a, n, R)
        b_ok = is_nth_power_up_to_unit(b, n, R)
        neg_Q = not (a_ok and b_ok)
    except Exception:
        neg_Q = False

    return [H1, H2, H3, H4, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: n is a positive integer",
    "H_3: The greatest common divisor of a and b is a unit",
    "H_4: ab = c^n",
    "¬Q: a and b are not both n-th powers up to a unit in R"
]

N_HYP = 4
NEG_Q_INDEX = 4