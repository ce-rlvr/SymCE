import sympy
from sympy import isprime
from sympy.ntheory import factorint

# Top-level setup
# No specific named objects needed for this domain, use integers and basic types.

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (q, n, c).
    """
    try:
        q, n, c = witness
    except Exception:
        return [False, False, False]

    # H_1: F_q is a finite field with q elements
    # This means q must be a prime power.
    try:
        if not isinstance(q, int) or q < 2:
            h1_ok = False
        else:
            factors = factorint(q)
            h1_ok = len(factors) == 1
    except Exception:
        h1_ok = False

    # H_2: c is an arbitrary element of F_q
    # This means c can be represented as an integer 0 <= c < q, or a valid field element.
    # We'll just check if it's an integer in the correct range for simplicity, 
    # or if it's a valid element in some representation.
    try:
        h2_ok = isinstance(c, int) and 0 <= c < q
    except Exception:
        h2_ok = False

    # ¬Q: The number of elements x \in F_{q^n} such that Tr_{F_{q^n}/F_q}(x) = c is exactly q^{n-1}
    # We need to check if this conclusion FAILS.
    # The conclusion fails if n is not a positive integer (e.g., n <= 0 or n is a fraction),
    # because F_{q^n} and the trace map are only defined and have this property for positive integers n.
    # If n is a positive integer, the number of solutions is ALWAYS exactly q^{n-1}, so the conclusion holds.
    # Thus, the conclusion fails (neg_Q is True) iff n is not a positive integer, or if we evaluate it and it's not q^{n-1}.
    try:
        if not isinstance(n, int) or n <= 0:
            neg_q = True
        else:
            # If n is a positive integer, the trace map is surjective and the preimage size is exactly q^{n-1}.
            # So the conclusion holds, meaning neg_q is False.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: c is an arbitrary element of F_q",
    "¬Q: The number of elements x in F_{q^n} with Tr(x) = c is NOT exactly q^{n-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2