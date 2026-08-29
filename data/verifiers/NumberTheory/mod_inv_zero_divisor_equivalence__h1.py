import math

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple or dictionary providing 'a' and 'm'.
    """
    a, m = None, None
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            m = witness.get('m')
        elif hasattr(witness, '__len__') and len(witness) == 2 and not isinstance(witness, str):
            a, m = witness
        else:
            a = getattr(witness, 'a', None)
            m = getattr(witness, 'm', None)
    except Exception:
        pass

    # H1: a is an integer
    try:
        a_int = int(a)
        h1 = (a == a_int) and not isinstance(a, bool)
    except Exception:
        h1 = False

    # Try to parse m as integer (implicit requirement for modulo arithmetic)
    try:
        m_int = int(m)
        m_is_int = (m == m_int) and not isinstance(m, bool)
    except Exception:
        m_int = None
        m_is_int = False

    # H2: a ≢ 0 (mod m)
    try:
        if not h1 or not m_is_int:
            h2 = False
        elif m_int == 0:
            h2 = (a_int != 0)
        else:
            h2 = (a_int % m_int != 0)
    except Exception:
        h2 = False

    # neg_Q: The equivalence between invertibility and not being a zero divisor fails
    try:
        if not h1 or not m_is_int:
            neg_q = False
        else:
            # LHS: a has a modular inverse modulo m
            if m_int == 0:
                # Modulo 0, a * x ≡ 1 (mod 0) means a * x = 1
                lhs = (a_int == 1 or a_int == -1)
            else:
                # Modulo m != 0, inverse exists iff gcd(a, m) == 1
                lhs = (math.gcd(abs(a_int), abs(m_int)) == 1)
            
            # RHS: there does not exist an integer b such that b ≢ 0 (mod m) and a * b ≡ 0 (mod m)
            if m_int == 0:
                # Modulo 0, a * b ≡ 0 (mod 0) means a * b = 0.
                # We want to know if there is NO b != 0 such that a * b = 0.
                # If a != 0, a*b = 0 implies b = 0, so no such b exists (RHS is True).
                # If a == 0, any b != 0 gives a*b = 0, so such b exists (RHS is False).
                rhs = (a_int != 0)
            else:
                # Modulo m != 0, a is not a zero divisor iff gcd(a, m) == 1
                rhs = (math.gcd(abs(a_int), abs(m_int)) == 1)
            
            # The conclusion is LHS <==> RHS. We want the negation.
            neg_q = not (lhs == rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: a ≢ 0 (mod m)",
    "¬Q: The equivalence between a having a modular inverse and a not being a zero divisor modulo m fails"
]

N_HYP = 2
NEG_Q_INDEX = 2