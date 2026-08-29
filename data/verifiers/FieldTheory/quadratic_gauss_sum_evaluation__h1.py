import sympy
from sympy import exp, I, pi, Rational
from sympy.ntheory import jacobi_symbol

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def kronecker(a, p):
    """
    Extension of the Legendre/Jacobi symbol to all integers p >= 1.
    """
    if p == 0:
        return 1 if abs(a) == 1 else 0
    if p == 1:
        return 1
    if p == 2:
        if a % 2 == 0:
            return 0
        return 1 if a % 8 in (1, 7) else -1
    if p % 2 == 0:
        return kronecker(a, 2) * kronecker(a, p // 2)
    return jacobi_symbol(a, p)

def conditions(witness):
    try:
        # The witness can be either a tuple (p, zeta_p, g) or just the integer p.
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            p, zeta, g = witness
        else:
            p = witness
            zeta = exp(2 * I * pi / p)
            g = sum(kronecker(a, p) * zeta**a for a in range(1, p))
    except Exception:
        return [False, False, False]

    def check_eq(a, b):
        try:
            diff = sympy.expand(a - b)
            if diff == 0:
                return True
            
            # Fast numerical check to avoid hanging on complex symbolic simplifications
            try:
                c_val = complex(diff.evalf(chop=True))
                if abs(c_val) < 1e-9:
                    return True
                if abs(c_val) > 1e-4:
                    return False
            except Exception:
                pass
                
            # Fallback to symbolic simplification
            diff = sympy.simplify(diff)
            if diff == 0:
                return True
        except Exception:
            pass
        return False

    # H_1: zeta_p is a primitive p-th root of unity
    h1 = False
    try:
        if isinstance(p, (int, sympy.Integer)) and p >= 1:
            if check_eq(zeta**p, 1):
                h1 = True
                if p > 1:
                    for q in sympy.primefactors(p):
                        if check_eq(zeta**(p // q), 1):
                            h1 = False
                            break
                else:
                    if not check_eq(zeta, 1):
                        h1 = False
    except Exception:
        h1 = False

    # H_2: g = sum_{a=1}^{p-1} (a|p) zeta_p^a
    h2 = False
    try:
        expected_g = sum(kronecker(a, p) * zeta**a for a in range(1, p))
        if check_eq(g, expected_g):
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: g^2 != (-1)^{(p-1)/2} p
    neg_q = False
    try:
        rhs = ((-1)**Rational(p - 1, 2)) * p
        if not check_eq(g**2, rhs):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_p is a primitive p-th root of unity",
    "H_2: g is the quadratic Gauss sum",
    "¬Q: g^2 is not equal to (-1)^{(p-1)/2} p"
]

N_HYP = 2
NEG_Q_INDEX = 2