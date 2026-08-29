import sympy
from sympy.ntheory import isprime

# Top-level setup
# The witness is expected to represent the field K, which we identify by its characteristic.
# We provide a helper to extract the characteristic from various possible witness formats.

def _get_p(witness):
    if isinstance(witness, float):
        raise ValueError("Float is not a valid characteristic")
    if isinstance(witness, str):
        digits = ''.join(c for c in witness if c.isdigit())
        if digits:
            return int(digits)
        upper_w = witness.upper()
        if 'Q' in upper_w or 'C' in upper_w or 'R' in upper_w:
            return 0
        raise ValueError("Cannot parse characteristic from string")
    try:
        return int(witness.characteristic())
    except Exception:
        pass
    try:
        return int(witness.characteristic)
    except Exception:
        pass
    try:
        return int(witness.char())
    except Exception:
        pass
    try:
        return int(witness.char)
    except Exception:
        pass
    return int(witness)

def conditions(witness) -> list[bool]:
    try:
        p = _get_p(witness)
        # H_1: K is an algebraically closed field.
        # We assume K is the algebraic closure of its prime field.
        # A valid characteristic must be 0 or a prime number.
        h1_ok = (p == 0) or isprime(p)
    except Exception:
        h1_ok = False

    try:
        # H_2: K((t)) is the field of formal Laurent series over K.
        # This is definitional and holds as long as K is a valid field.
        h2_ok = h1_ok
    except Exception:
        h2_ok = False

    try:
        p = _get_p(witness)
        # ¬Q: The algebraic closure of K((t)) is NOT isomorphic to the field of Puiseux series.
        # The Newton-Puiseux theorem fails in positive characteristic (p > 0).
        # For example, the Artin-Schreier polynomial x^p - x - t^(-1) has no root in the Puiseux series field.
        neg_q_ok = h1_ok and (p > 0)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: K((t)) is the field of formal Laurent series over K",
    "¬Q: The algebraic closure of K((t)) is not isomorphic to the field of Puiseux series"
]

N_HYP = 2
NEG_Q_INDEX = 2