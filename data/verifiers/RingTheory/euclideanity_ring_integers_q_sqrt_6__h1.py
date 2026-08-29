import sympy
from sympy.ntheory import factorint

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: K is a valid quadratic field (witnessed by squarefree integer d != 1)",
    "¬Q: The ring of integers of K is not a Euclidean domain"
]

def is_squarefree_int(n):
    if n == 0:
        return False
    factors = factorint(abs(n))
    return all(exp == 1 for exp in factors.values())

def get_d(witness):
    try:
        if isinstance(witness, tuple) and len(witness) > 0:
            witness = witness[0]
            
        if isinstance(witness, int):
            return witness
        if isinstance(witness, str):
            try:
                return int(witness)
            except ValueError:
                pass
        if hasattr(witness, 'is_Integer') and witness.is_Integer:
            return int(witness)
        if isinstance(witness, sympy.Expr):
            if witness.func == sympy.sqrt:
                arg = witness.args[0]
                if arg.is_Integer:
                    return int(arg)
            if witness.func == sympy.Pow:
                base, exp = witness.args
                if base.is_Integer and exp == sympy.Rational(1, 2):
                    return int(base)
        if hasattr(witness, 'ext') and hasattr(witness.ext, 'minpoly'):
            poly = witness.ext.minpoly
            if poly.degree() == 2:
                coeffs = poly.all_coeffs()
                if len(coeffs) == 3 and coeffs[0] == 1 and coeffs[1] == 0:
                    return int(-coeffs[2])
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    try:
        d = get_d(witness)
        if d is None:
            h1_ok = False
        else:
            h1_ok = bool((d not in (0, 1)) and is_squarefree_int(d))
    except Exception:
        h1_ok = False

    try:
        d = get_d(witness)
        if d is None:
            neg_q_ok = False
        else:
            if d < 0:
                # The only imaginary quadratic fields that are Euclidean are for d in {-1, -2, -3, -7, -11}
                neg_q_ok = bool(d not in [-1, -2, -3, -7, -11])
            else:
                # Known Euclidean real quadratic fields
                known_euclidean_pos = {2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 29, 33, 37, 41, 57, 69, 73}
                neg_q_ok = bool(d not in known_euclidean_pos)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]