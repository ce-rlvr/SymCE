import sympy
from sympy import Poly, degree
from sympy.abc import x
from sympy.ntheory import factorint
import math

def is_irred_over_Fq(f, q):
    if not (isinstance(q, int) and q >= 2):
        return False
    factors = factorint(q)
    if len(factors) != 1:
        return False
    p = list(factors.keys())[0]
    k = factors[p]
    try:
        f_poly = Poly(f, x, domain='ZZ')
        fact = sympy.factor_list(f_poly, modulus=p)
        is_irred_p = (len(fact[1]) == 1 and fact[1][0][1] == 1)
        if k == 1:
            return bool(is_irred_p)
        else:
            d = degree(f_poly)
            return bool(is_irred_p and math.gcd(d, k) == 1)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            f = witness.get('f')
            m = witness.get('m')
            n = witness.get('n', None)
        else:
            if len(witness) == 4:
                q, f, n, m = witness
            elif len(witness) == 3:
                q, f, m = witness
                n = None
            else:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if isinstance(q, int) and q >= 2:
            factors = factorint(q)
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = is_irred_over_Fq(f, q)
    except Exception:
        h2 = False

    try:
        d = degree(Poly(f, x))
        if n is None:
            n_val = d
        else:
            n_val = n
        h3 = isinstance(m, int) and m >= 1 and math.gcd(n_val, m) == 1
        if n is not None:
            h3 = h3 and (n == d)
    except Exception:
        h3 = False

    try:
        if not h1:
            neg_q = False
        elif not is_irred_over_Fq(f, q):
            neg_q = True
        else:
            d = degree(Poly(f, x))
            neg_q = math.gcd(d, m) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: f is an irreducible polynomial over F_q",
    "H_3: m >= 1 is an integer such that gcd(n, m) == 1",
    "not_Q: f is not irreducible over the extension field F_q^m"
]

N_HYP = 3
NEG_Q_INDEX = 3