import sympy
import math

def _is_int(x):
    return isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            p = witness.get('p')
            e = witness.get('e')
            f = witness.get('f')
        else:
            a, b, p, e, f = witness
    except Exception:
        return [False] * 5

    # H1: a and b are positive integers
    try:
        h1 = _is_int(a) and _is_int(b) and a > 0 and b > 0
    except Exception:
        h1 = False

    # H2: p, e, f are sequences of the same length and p_i are integers
    try:
        h2 = (isinstance(p, (list, tuple)) and isinstance(e, (list, tuple)) and isinstance(f, (list, tuple)) and
              len(p) == len(e) == len(f) and
              all(_is_int(pi) for pi in p))
    except Exception:
        h2 = False

    # H3: e_i >= 0 and f_i >= 0 are integers
    try:
        h3 = (all(_is_int(ei) and ei >= 0 for ei in e) and
              all(_is_int(fi) and fi >= 0 for fi in f))
    except Exception:
        h3 = False

    # H4: a = p_1^{e_1} ... p_r^{e_r} and b = p_1^{f_1} ... p_r^{f_r}
    try:
        prod_a = 1
        for pi, ei in zip(p, e):
            prod_a *= pi ** ei
        prod_b = 1
        for pi, fi in zip(p, f):
            prod_b *= pi ** fi
        h4 = (a == prod_a) and (b == prod_b)
    except Exception:
        h4 = False

    # Neg_Q: lcm(a, b) != prod p_i^{max(e_i, f_i)}
    try:
        lcm_ab = sympy.lcm(a, b)
        prod_lcm = 1
        for pi, ei, fi in zip(p, e, f):
            prod_lcm *= pi ** max(ei, fi)
        neg_q = (lcm_ab != prod_lcm)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "H_2: p, e, f are sequences of the same length and p_i are integers",
    "H_3: e_i >= 0 and f_i >= 0 are integers",
    "H_4: a and b are given by the products of p_i^e_i and p_i^f_i respectively",
    "¬Q: lcm(a, b) is not equal to the product of p_i^max(e_i, f_i)"
]

N_HYP = 4
NEG_Q_INDEX = 4