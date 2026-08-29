import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The witness should be a tuple (a, b, m).
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            m = witness.get('m')
        else:
            a, b, m = witness
    except Exception:
        return [False, False]

    # H1: For every integer x, ax \equiv b \pmod m
    h1_ok = True
    try:
        # Check for a range of integers to ensure the identity holds
        for i in range(-20, 21):
            if m == 0:
                # Congruence modulo 0 is strict equality
                if a * i != b:
                    h1_ok = False
                    break
            else:
                if (a * i - b) % m != 0:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # Q: m divides a and m divides b
    try:
        if m == 0:
            # By strict definition, 0 does not divide any integer (including 0)
            m_divides_a = False
            m_divides_b = False
        else:
            m_divides_a = (a % m == 0)
            m_divides_b = (b % m == 0)
            
        neg_q_ok = not (m_divides_a and m_divides_b)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: For every integer x, ax \\equiv b \\pmod m",
    "¬Q: m does not divide a or m does not divide b"
]

N_HYP = 1
NEG_Q_INDEX = 1