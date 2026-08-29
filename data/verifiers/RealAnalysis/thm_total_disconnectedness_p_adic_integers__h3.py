import sympy

# Top-level setup
# No specific named objects needed for this number theory / topology statement.

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the given witness.
    The witness is expected to be a prime number p.
    """
    try:
        if isinstance(witness, (tuple, list)):
            p = witness[0]
        elif isinstance(witness, dict):
            p = witness.get("p", witness)
        else:
            p = witness
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H2 is definitional: Let Z_p be the set of p-adic integers.
    h2 = True

    # Conclusion: Z_p is a totally disconnected topological space.
    # For any prime p, the p-adic integers Z_p with the standard p-adic topology
    # is totally disconnected. Therefore, the conclusion is always true for valid p,
    # meaning the negated conclusion is always false.
    neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: Z_p is the set of p-adic integers",
    "¬Q: Z_p is not a totally disconnected topological space"
]

N_HYP = 2
NEG_Q_INDEX = 2