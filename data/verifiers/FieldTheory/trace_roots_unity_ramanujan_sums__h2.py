import sympy as sp

# Top-level setup
# No special named objects needed for this number theory / field theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Given a witness (n, k), checks if it is a valid counterexample to the conjecture.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        # Witness should be a tuple or list of two elements: (n, k)
        if len(witness) != 2:
            return [False, False, False]
        n, k = witness
    except Exception:
        return [False, False, False]

    # Hypothesis 1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    # Hypothesis 2: k is an integer
    try:
        h2_ok = isinstance(k, int)
    except Exception:
        h2_ok = False

    # Conclusion: The field trace Tr_{Q(zeta_n)/Q}(zeta_n^k) is equal to the Ramanujan sum
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            # Compute the field trace of zeta_n^k in Q(zeta_n)/Q
            # The trace is the sum of the Galois conjugates: zeta_n^{a*k} for gcd(a, n) == 1
            trace_val = 0
            for a in range(1, n + 1):
                if sp.gcd(a, n) == 1:
                    # Using exact symbolic representation
                    trace_val += sp.exp(2 * sp.I * sp.pi * a * k / n)
            
            # The trace is always an integer. We simplify and extract it.
            trace_val = sp.simplify(trace_val)
            # In case of minor floating point artifacts in symbolic simplification, round it
            trace_int = round(complex(trace_val).real)

            # Compute the Ramanujan sum using the given formula: sum_{d | gcd(k,n)} d * mu(n/d)
            g = sp.gcd(k, n)
            ram_sum = 0
            for d in sp.divisors(g):
                ram_sum += d * sp.mobius(n // d)

            # The conclusion FAILS if the trace is NOT equal to the Ramanujan sum
            neg_q_ok = (trace_int != ram_sum)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: k is an integer",
    "¬Q: The field trace Tr_{Q(zeta_n)/Q}(zeta_n^k) is NOT equal to the Ramanujan sum sum_{d | gcd(k,n)} d * mu(n/d)"
]

N_HYP = 2
NEG_Q_INDEX = 2