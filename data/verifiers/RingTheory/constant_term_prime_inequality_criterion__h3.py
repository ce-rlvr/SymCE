import sympy
from sympy import Poly, Symbol, factor_list, isprime

x = Symbol('x')

def conditions(witness):
    try:
        f = Poly(witness, x, domain='ZZ')
        h1_ok = bool(f.degree() >= 1)
    except Exception:
        h1_ok = False

    try:
        f = Poly(witness, x, domain='ZZ')
        a0 = f.nth(0)
        h2_ok = bool(isprime(a0))
    except Exception:
        h2_ok = False

    try:
        f_qq = Poly(witness, x, domain='QQ')
        if f_qq.degree() < 1:
            neg_q_ok = True
        else:
            factors = factor_list(f_qq, domain='QQ')[1]
            neg_q_ok = bool(sum(mult for _, mult in factors) > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ['H_1: deg>=1', 'H_2: a0 prime', 'not Q: reducible']
N_HYP = 2
NEG_Q_INDEX = 2