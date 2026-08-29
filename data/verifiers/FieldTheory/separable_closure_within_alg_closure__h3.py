import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks whether the given witness satisfies the remaining hypotheses
    and fails the conclusion of the conjecture.
    
    Since SymPy does not natively support operations like algebraic closures
    or separable closures for arbitrary fields, the witness is expected to be
    a mock object (e.g., a dictionary or a tuple) that provides the truth values
    for the properties.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('F_is_field', witness.get('is_field', False)))
            h2 = bool(witness.get('F_bar_is_algebraic_closure', witness.get('is_algebraic_closure', False)))
            
            q_subfield = bool(witness.get('F_sep_is_subfield', witness.get('is_subfield', True)))
            q_sep_closed = bool(witness.get('F_sep_is_separably_closed', witness.get('is_separably_closed', True)))
            
            # The conclusion is that F^{sep} is a subfield AND is separably closed.
            # We negate this for neg_Q.
            neg_q = not (q_subfield and q_sep_closed)
            
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 3:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            q = bool(witness[2])
            return [h1, h2, not q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: \\overline{F} is an algebraic closure of F",
    "¬Q: F^{sep} is not a subfield of \\overline{F} or is not separably closed"
]

N_HYP = 2
NEG_Q_INDEX = 2