import sympy as sp
from sympy import Symbol, solveset, S, singularities

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The witness can be a SymPy expression `f` (assuming domain is Reals),
    or a tuple `(f, domain)` where domain is a SymPy set.
    """
    if isinstance(witness, tuple):
        f, domain = witness
    else:
        f = witness
        domain = S.Reals

    # H1: Let C^infty(M) be the ring of smooth real-valued functions on M under pointwise operations
    # This is a definitional hypothesis, so it always holds.
    h1 = True

    # H2: Let f be an element of C^infty(M)
    try:
        sings = singularities(f, x)
        # f is smooth if it has no singularities in the domain
        h2 = sings.intersect(domain).is_empty
        if h2 is None:
            h2 = False
    except Exception:
        h2 = False

    # Conclusion: f is a unit in C^infty(M) if and only if f(p) != 0 for all p in M
    try:
        # Check if f(p) != 0 for all p in M
        zeros = solveset(f, x, domain=domain)
        is_never_zero = (zeros == S.EmptySet)

        # Check if f is a unit in C^infty(M)
        # f is a unit iff 1/f is in C^infty(M), which means 1/f is smooth on M
        inv_sings = singularities(1/f, x)
        is_unit = inv_sings.intersect(domain).is_empty
        if is_unit is None:
            is_unit = False

        # The conclusion fails if the equivalence does not hold
        neg_q = not (is_unit == is_never_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: C^infty(M) is the ring of smooth real-valued functions on M",
    "H_2: f is an element of C^infty(M)",
    "¬Q: f is a unit in C^infty(M) is NOT equivalent to f(p) != 0 for all p in M"
]

N_HYP = 2
NEG_Q_INDEX = 2