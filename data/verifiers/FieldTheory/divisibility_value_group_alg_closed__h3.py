import sympy
from sympy import S

# Top-level setup for potential witness expressions
CC = S.Complexes
QQ = S.Rationals
RR = S.Reals
ZZ = S.Integers

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Since SymPy does not natively implement algebraically closed valued fields and their 
    value groups, the witness is expected to be a dictionary or an object exposing 
    the relevant boolean properties.
    """
    def get_prop(obj, names, default):
        if isinstance(obj, dict):
            for name in names:
                if name in obj:
                    return obj[name]
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)
        return default

    # H_1: K is an algebraically closed field
    try:
        if isinstance(witness, tuple) and len(witness) >= 1 and witness[0] == CC:
            h1 = True
        else:
            h1 = bool(get_prop(witness, [
                'is_algebraically_closed_field', 
                'is_algebraically_closed', 
                'algebraically_closed'
            ], False))
    except Exception:
        h1 = False

    # H_2: v is a valuation on K
    try:
        h2 = bool(get_prop(witness, [
            'is_valuation', 
            'has_valuation', 
            'valuation',
            'is_valued_field'
        ], False))
    except Exception:
        h2 = False

    # ¬Q: Gamma is NOT a divisible abelian group
    try:
        is_divisible = bool(get_prop(witness, [
            'value_group_is_divisible', 
            'is_divisible', 
            'divisible_value_group', 
            'Gamma_is_divisible'
        ], True))
        neg_q = not is_divisible
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: v is a valuation on K",
    "¬Q: Gamma is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2