import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: There are infinitely many distinct prime elements that divide a"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # The witness can be a tuple (R, a) or just the element a (with R implicitly ZZ)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, a = witness
    else:
        R = ZZ
        a = witness

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # ¬Q: There are infinitely many distinct prime elements that divide a.
    # In a UFD, a non-zero element has only finitely many prime divisors.
    # If a == 0, every prime element divides a. Thus, if R is a UFD but not a field,
    # it typically has infinitely many prime elements (e.g., ZZ, QQ[x]), making ¬Q True.
    try:
        is_zero = False
        try:
            is_zero = bool(a == 0)
        except Exception:
            pass
            
        if not is_zero and hasattr(R, 'zero'):
            try:
                is_zero = bool(a == R.zero)
            except Exception:
                pass

        if is_zero:
            # Fields have no prime elements, so 0 prime divisors (which is finite).
            if getattr(R, 'is_Field', False):
                neg_q = False
            else:
                # For non-field UFDs like ZZ or polynomial rings, there are infinitely many primes.
                neg_q = True
        else:
            # Non-zero elements in a UFD have finitely many prime divisors.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]