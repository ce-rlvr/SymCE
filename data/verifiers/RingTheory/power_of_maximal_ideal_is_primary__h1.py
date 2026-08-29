import sympy
from sympy import symbols
from sympy.abc import x, y, z

# Top-level setup
# (No specific named rings are required for this general verifier, 
# but we provide standard symbols just in case the witness uses them)

CONDITION_LABELS = [
    "H_1: M is a maximal ideal of R",
    "H_2: n is a positive integer",
    "¬Q: The ideal M^n is not an M-primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False

    # 1. If witness is a dictionary
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_maximal_ideal', witness.get('M_is_maximal', False)))
            h2 = isinstance(witness.get('n'), int) and witness.get('n') > 0
            is_primary = witness.get('is_M_primary', witness.get('is_primary', True))
            neg_q = not bool(is_primary)
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. If witness is a callable
    if callable(witness):
        try:
            res = witness()
            if isinstance(res, (list, tuple)) and len(res) == 3:
                return list(res)
        except Exception:
            pass

    # 3. If witness is an object with attributes
    try:
        if hasattr(witness, 'is_maximal_ideal'):
            h1 = bool(witness.is_maximal_ideal() if callable(witness.is_maximal_ideal) else witness.is_maximal_ideal)
        elif hasattr(witness, 'M_is_maximal'):
            h1 = bool(witness.M_is_maximal() if callable(witness.M_is_maximal) else witness.M_is_maximal)
        elif hasattr(witness, 'M') and hasattr(witness.M, 'is_maximal'):
            h1 = bool(witness.M.is_maximal(witness.R) if hasattr(witness, 'R') else witness.M.is_maximal())
    except Exception:
        pass

    try:
        if hasattr(witness, 'n'):
            n_val = witness.n() if callable(witness.n) else witness.n
            h2 = isinstance(n_val, int) and n_val > 0
    except Exception:
        pass

    try:
        is_primary = True
        if hasattr(witness, 'is_M_primary'):
            is_primary = bool(witness.is_M_primary() if callable(witness.is_M_primary) else witness.is_M_primary)
        elif hasattr(witness, 'Mn_is_primary'):
            is_primary = bool(witness.Mn_is_primary() if callable(witness.Mn_is_primary) else witness.Mn_is_primary)
        elif hasattr(witness, 'is_primary'):
            if callable(witness.is_primary):
                try:
                    is_primary = bool(witness.is_primary())
                except TypeError:
                    is_primary = bool(witness.is_primary(getattr(witness, 'M', None), getattr(witness, 'n', None)))
            else:
                is_primary = bool(witness.is_primary)
        elif hasattr(witness, 'Mn') and hasattr(witness.Mn, 'is_primary'):
            is_primary = bool(witness.Mn.is_primary())
        neg_q = not is_primary
    except Exception:
        pass

    # 4. If witness is a tuple
    if isinstance(witness, tuple):
        try:
            if len(witness) == 3:
                R, M, n = witness
                if hasattr(M, 'is_maximal'):
                    h1 = bool(M.is_maximal(R))
                h2 = isinstance(n, int) and n > 0
                if hasattr(M, '__pow__'):
                    Mn = M ** n
                    if hasattr(Mn, 'is_M_primary'):
                        is_primary = bool(Mn.is_M_primary(R))
                    elif hasattr(Mn, 'is_primary'):
                        is_primary = bool(Mn.is_primary(R))
                    else:
                        is_primary = True
                    neg_q = not is_primary
            elif len(witness) == 2:
                M, n = witness
                if hasattr(M, 'is_maximal'):
                    h1 = bool(M.is_maximal())
                h2 = isinstance(n, int) and n > 0
                if hasattr(M, '__pow__'):
                    Mn = M ** n
                    if hasattr(Mn, 'is_M_primary'):
                        is_primary = bool(Mn.is_M_primary())
                    elif hasattr(Mn, 'is_primary'):
                        is_primary = bool(Mn.is_primary())
                    else:
                        is_primary = True
                    neg_q = not is_primary
        except Exception:
            pass

    return [h1, h2, neg_q]