import sympy
from sympy import symbols, S

# Top-level setup for FieldTheory
x, y, z = symbols('x y z')
QQ = S.Rationals
ZZ = S.Integers
RR = S.Reals
CC = S.Complexes

CONDITION_LABELS = [
    "H_1: F is a countable set",
    "H_2: K is the algebraic closure of F",
    "¬Q: K is not a countable set"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    F, K = None, None
    h2 = False
    
    # Extract F and K from the witness, and verify H_2
    if isinstance(witness, tuple) and len(witness) == 2:
        F, K = witness
        try:
            if callable(F.algebraic_closure):
                h2 = bool(K == F.algebraic_closure())
            else:
                h2 = bool(K == F.algebraic_closure)
        except Exception:
            h2 = False
    elif isinstance(witness, dict) and 'F' in witness and 'K' in witness:
        F = witness['F']
        K = witness['K']
        try:
            if callable(F.algebraic_closure):
                h2 = bool(K == F.algebraic_closure())
            else:
                h2 = bool(K == F.algebraic_closure)
        except Exception:
            h2 = False
    else:
        # Try to treat the witness itself as F
        F = witness
        try:
            if callable(F.algebraic_closure):
                K = F.algebraic_closure()
            else:
                K = F.algebraic_closure
            h2 = True
        except Exception:
            # Try to treat the witness as an object with F and K attributes
            try:
                F = witness.F
                K = witness.K
                if callable(F.algebraic_closure):
                    h2 = bool(K == F.algebraic_closure())
                else:
                    h2 = bool(K == F.algebraic_closure)
            except Exception:
                h2 = False

    # H_1: F is a countable set
    try:
        if callable(F.is_countable):
            h1 = bool(F.is_countable())
        else:
            h1 = bool(F.is_countable)
    except Exception:
        h1 = False

    # ¬Q: K is not a countable set
    try:
        if callable(K.is_countable):
            neg_q = not bool(K.is_countable())
        else:
            neg_q = not bool(K.is_countable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]