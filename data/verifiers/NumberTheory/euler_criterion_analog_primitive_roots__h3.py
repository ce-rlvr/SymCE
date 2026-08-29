import sympy
from sympy.ntheory import totient, primitive_root

def conditions(witness):
    """
    Given a witness (n, a), checks if it is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, a = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: n is an integer strictly greater than 2
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) > 2
    except Exception:
        h1 = False

    # H2: n possesses at least one primitive root
    try:
        if h1:
            # primitive_root raises ValueError if no primitive root exists
            primitive_root(int(n))
            h2 = True
        else:
            h2 = False
    except ValueError:
        h2 = False
    except Exception:
        h2 = False

    # neg_Q: a^{\phi(n)/2} \not\equiv -1 \pmod n
    try:
        if h1 and isinstance(a, (int, sympy.Integer)):
            n_int = int(n)
            a_int = int(a)
            phi = totient(n_int)
            # For n > 2, phi(n) is always even, so integer division is exact.
            val = pow(a_int, phi // 2, n_int)
            # -1 mod n is n - 1
            neg_q = (val != n_int - 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "H_2: n possesses at least one primitive root",
    "¬Q: a^{\\phi(n)/2} \\not\\equiv -1 \\pmod n"
]

N_HYP = 2
NEG_Q_INDEX = 2