import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Unpack the witness. It should provide a, m, and n.
        if isinstance(witness, dict):
            a = witness['a']
            m = witness['m']
            n = witness['n']
        elif hasattr(witness, 'a') and hasattr(witness, 'm') and hasattr(witness, 'n'):
            a = witness.a
            m = witness.m
            n = witness.n
        else:
            a, m, n = witness
            
        # Ensure they are integers
        a_int = int(a)
        m_int = int(m)
        n_int = int(n)
        if a_int != a or m_int != m or n_int != n:
            return [False, False]
        a, m, n = a_int, m_int, n_int
    except Exception:
        return [False, False]

    # H_1: a is an integer such that gcd(a, m) = 1
    try:
        h1 = (math.gcd(a, m) == 1)
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist an integer x such that x = a (mod m) and gcd(x, n) = 1
    # Proof of logic:
    # If n != 0, by Dirichlet's theorem / CRT, such an x always exists, so the conclusion holds (neg_Q is False).
    # If n == 0, we need gcd(x, 0) = 1, which implies |x| = 1, so x must be 1 or -1.
    # Thus, if n == 0, the conclusion fails iff neither 1 nor -1 is congruent to a modulo m.
    try:
        if n != 0:
            neg_q = False
        else:
            if m == 0:
                neg_q = (a != 1 and a != -1)
            else:
                neg_q = ((a - 1) % m != 0) and ((a + 1) % m != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer such that gcd(a, m) = 1",
    "¬Q: There does not exist an integer x such that x ≡ a (mod m) and gcd(x, n) = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1