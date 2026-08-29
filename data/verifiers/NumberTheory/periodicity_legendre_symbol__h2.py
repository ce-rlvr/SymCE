import sympy
from sympy import isprime
from sympy.ntheory import legendre_symbol

# Top-level setup
# No specific named bindings are required for this number theory problem.

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, b, p), checks if it is a valid counterexample to the false conjecture.
    The dropped hypothesis was "a is an integer".
    """
    try:
        a, b, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is an odd prime
    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    # H_2: b is an integer
    try:
        if isinstance(b, int):
            h2 = True
        elif hasattr(b, 'is_integer'):
            if callable(b.is_integer):
                h2 = bool(b.is_integer())
            else:
                h2 = bool(b.is_integer)
        elif hasattr(b, 'denominator') and b.denominator == 1:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: a \equiv b \pmod p
    # Since 'a' might be a rational number (the dropped hypothesis), we check congruence for rationals.
    try:
        if isinstance(a, sympy.Float):
            a_val = sympy.Rational(a)
        else:
            a_val = a
            
        if hasattr(a_val, 'p') and hasattr(a_val, 'q'):
            num, den = a_val.p, a_val.q
            h3 = bool((den % p != 0) and ((num - b * den) % p == 0))
        elif hasattr(a_val, 'numerator') and hasattr(a_val, 'denominator'):
            num, den = a_val.numerator, a_val.denominator
            h3 = bool((den % p != 0) and ((num - b * den) % p == 0))
        elif hasattr(a_val, 'as_integer_ratio'):
            num, den = a_val.as_integer_ratio()
            h3 = bool((den % p != 0) and ((num - b * den) % p == 0))
        else:
            h3 = bool((a_val - b) % p == 0)
    except Exception:
        h3 = False

    # ¬Q: (a/p) != (b/p)
    # If 'a' is not an integer, the Legendre symbol is undefined and will raise an exception,
    # meaning the conclusion fails (so its negation is True).
    try:
        try:
            la = legendre_symbol(a, p)
            lb = legendre_symbol(b, p)
            q = (la == lb)
        except Exception:
            q = False
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: b is an integer",
    "H_3: a is congruent to b modulo p",
    "¬Q: Legendre symbol (a/p) is not equal to (b/p) or is undefined"
]

N_HYP = 3
NEG_Q_INDEX = 3