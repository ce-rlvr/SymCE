import sympy
import math

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the RSA congruence conjecture.
    The witness is expected to provide p, q, e, d, M, and optionally n.
    If n is not provided, it defaults to p * q.
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            q = witness['q']
            e = witness['e']
            d = witness['d']
            M = witness['M']
            n = witness.get('n')
            if n is None:
                n = p * q
        elif hasattr(witness, 'p'):
            p = witness.p
            q = witness.q
            e = witness.e
            d = witness.d
            M = witness.M
            n = getattr(witness, 'n', None)
            if n is None:
                n = p * q
        else:
            if len(witness) == 6:
                p, q, e, d, M, n = witness
            elif len(witness) == 5:
                p, q, e, d, M = witness
                n = p * q
            else:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: p and q are distinct prime numbers
    try:
        h1 = bool(sympy.isprime(p) and sympy.isprime(q) and p != q)
    except Exception:
        h1 = False

    # H2: e and d are positive integers such that ed \equiv 1 \pmod{\operatorname{lcm}(p-1, q-1)}
    try:
        if isinstance(e, (int, sympy.Integer)) and isinstance(d, (int, sympy.Integer)) and e > 0 and d > 0:
            L = sympy.lcm(int(p) - 1, int(q) - 1)
            h2 = bool((int(e) * int(d)) % L == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: M is an integer
    try:
        h3 = isinstance(M, (int, sympy.Integer)) and not isinstance(M, bool)
    except Exception:
        h3 = False

    # neg_Q: M^{ed} \not\equiv M \pmod n
    try:
        if not isinstance(n, (int, sympy.Integer)) or isinstance(n, bool):
            # If n is not an integer, congruence modulo n is undefined, so the conclusion fails.
            neg_q = True
        elif n == 0:
            if int(e) * int(d) > 1000000:
                neg_q = False  # Prevent timeout for huge exponents
            else:
                neg_q = bool((int(M) ** (int(e) * int(d))) != int(M))
        else:
            neg_q = bool(pow(int(M), int(e) * int(d), abs(int(n))) != (int(M) % abs(int(n))))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: e and d are positive integers such that ed \\equiv 1 \\pmod{\\operatorname{lcm}(p-1, q-1)}",
    "H_3: M is an integer",
    "¬Q: M^{ed} \\not\\equiv M \\pmod n"
]

N_HYP = 3
NEG_Q_INDEX = 3