import sympy
from sympy import S

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            m = witness.get('m')
            k = witness.get('k')
        else:
            a, b, m, k = witness
    except Exception:
        return [False, False, False]

    # H1: a, b, m are integers with m > 0
    h1_ok = False
    try:
        a_val = S(a)
        b_val = S(b)
        m_val = S(m)
        if a_val.is_integer and b_val.is_integer and m_val.is_integer and m_val > 0:
            h1_ok = True
    except Exception:
        pass

    # H2: a \equiv b \pmod m
    h2_ok = False
    try:
        if (S(a) - S(b)) % S(m) == 0:
            h2_ok = True
    except Exception:
        pass

    # neg_Q: a^k \not\equiv b^k \pmod m
    neg_q_ok = False
    try:
        ak = S(a)**S(k)
        bk = S(b)**S(k)
        if ak.is_integer and bk.is_integer:
            if (ak - bk) % S(m) != 0:
                neg_q_ok = True
        else:
            neg_q_ok = True
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a, b, m are integers with m > 0",
    "H_2: a = b (mod m)",
    "¬Q: a^k != b^k (mod m) or a^k, b^k are not integers"
]

N_HYP = 2
NEG_Q_INDEX = 2