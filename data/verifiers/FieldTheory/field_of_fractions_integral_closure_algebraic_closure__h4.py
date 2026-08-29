import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import Domain

# Top-level setup for witness expressions
x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: K_bar is the algebraic closure of K",
    "¬Q: The field of fractions of S is not exactly K_bar"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should provide the rings R and S, e.g., as a tuple (R, S) or a dict.
    """
    if isinstance(witness, dict):
        R = witness.get('R')
        S = witness.get('S')
    elif isinstance(witness, tuple):
        if len(witness) == 2:
            R, S = witness
        elif len(witness) >= 4:
            R = witness[0]
            S = witness[-1]
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: R is an integral domain
    try:
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        K = R.get_field() if hasattr(R, 'get_field') else None
        h2 = (K is not None)
    except Exception:
        h2 = False

    # H_3: K_bar is the algebraic closure of K
    try:
        # The algebraic closure of a field always exists mathematically.
        h3 = h2
    except Exception:
        h3 = False

    # ¬Q: The field of fractions of S is not exactly K_bar
    try:
        try:
            F_S = S.get_field() if hasattr(S, 'get_field') else None
        except Exception:
            F_S = None
            
        if F_S is None:
            is_alg_closure = False
        elif F_S == CC:
            # CC is the algebraic closure of RR and CC
            if K in (RR, CC):
                is_alg_closure = True
            else:
                is_alg_closure = False
        elif F_S in (QQ, RR, ZZ):
            # These are definitively not algebraically closed
            is_alg_closure = False
        else:
            # For other SymPy domains, they are generally not algebraically closed
            # unless explicitly constructed, which SymPy lacks a general domain for.
            is_alg_closure = False
            
        neg_q = not is_alg_closure
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]