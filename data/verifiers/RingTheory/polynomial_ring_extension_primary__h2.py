import sympy
from sympy import symbols

x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks whether the given witness satisfies the hypotheses and FAILS the conclusion.
    Order of return: [H_1, H_2, H_3, neg_Q]
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', witness.get('R_is_commutative', False)))
            h2 = bool(witness.get('P_is_prime', False))
            h3 = bool(witness.get('Q_is_P_primary', False))
            neg_q = not bool(witness.get('Qx_is_Px_primary', True))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'R_is_commutative') or hasattr(witness, 'P_is_prime'):
            h1 = bool(getattr(witness, 'is_commutative', getattr(witness, 'R_is_commutative', False)))
            h2 = bool(getattr(witness, 'P_is_prime', False))
            h3 = bool(getattr(witness, 'Q_is_P_primary', False))
            neg_q = not bool(getattr(witness, 'Qx_is_Px_primary', True))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal in R",
    "H_3: Q is a P-primary ideal",
    "neg_Q: The extension ideal Q(x) is not a P(x)-primary ideal in the polynomial ring R(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3