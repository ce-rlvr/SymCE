import sympy
from sympy import Symbol, limit, S

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample.
    The witness is expected to be a tuple (f, a, b, c) or a dictionary with these keys,
    where f is a sympy expression in terms of x, and a, b, c are real numbers.
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
        else:
            f, a, b, c = witness
    except Exception:
        return [False, False, False]

    # H_1: c is in the open interval (a, b)
    try:
        h1 = bool(a < c and c < b)
    except Exception:
        h1 = False

    # H_2: f is discontinuous at c
    try:
        L_left = limit(f, x, c, dir='-')
        L_right = limit(f, x, c, dir='+')
        val = f.subs(x, c)
        
        # A function is continuous at c if the left limit, right limit, and function value 
        # all exist, are finite, and are equal to each other.
        is_continuous = (
            (L_left.is_finite == True) and 
            (L_right.is_finite == True) and 
            (val.is_finite == True) and 
            (L_left == L_right) and 
            (L_left == val)
        )
        h2 = not is_continuous
    except Exception:
        h2 = False

    # ¬Q: The left-hand limit and right-hand limit at c both exist as distinct finite values
    try:
        L_left = limit(f, x, c, dir='-')
        L_right = limit(f, x, c, dir='+')
        
        neg_q = bool(
            (L_left.is_finite == True) and 
            (L_right.is_finite == True) and 
            (L_left != L_right)
        )
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: c is in the open interval (a, b)",
    "H_2: f is discontinuous at c",
    "¬Q: The left-hand limit and right-hand limit at c both exist as distinct finite values"
]

N_HYP = 2
NEG_Q_INDEX = 2