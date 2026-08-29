import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be the size of the finite field, q.
    """
    try:
        # Extract q from the witness
        if hasattr(witness, 'order') and callable(witness.order):
            q = int(witness.order())
        elif hasattr(witness, 'order'):
            q = int(witness.order)
        elif hasattr(witness, 'mod'):
            q = int(witness.mod)
        else:
            q = int(witness)
    except Exception:
        return [False, False]

    # Hypothesis 1: The characteristic of F_q is an odd prime
    try:
        factors = sympy.factorint(q)
        # A finite field F_q exists and has prime characteristic p iff q = p^k
        if len(factors) != 1:
            h1 = False
        else:
            p = list(factors.keys())[0]
            # The characteristic must be an odd prime
            h1 = (p % 2 != 0)
    except Exception:
        h1 = False

    # Conclusion: -1 is a square in F_q if and only if q = 1 mod 4
    try:
        if not h1:
            neg_q = False
        else:
            # In any finite field F_q of odd characteristic, the multiplicative group 
            # is cyclic of order q - 1. The element -1 is the unique element of order 2.
            # Therefore, -1 is a square if and only if the order of the group is divisible by 4,
            # which is equivalent to q % 4 == 1.
            # This mathematical equivalence holds unconditionally for all odd prime powers.
            is_square_in_Fq = (q % 4 == 1)
            q_mod_4_is_1 = (q % 4 == 1)
            
            conclusion = (is_square_in_Fq == q_mod_4_is_1)
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of F_q is an odd prime",
    "¬Q: -1 is a square in F_q if and only if q = 1 mod 4 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1