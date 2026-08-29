import sympy
import sympy.ntheory

# Top-level setup
# (No specific named objects required for this number theory problem)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture.
    The conjecture claims a formula for the Legendre symbol (-2/p) based on p mod 8,
    but it dropped the hypothesis that p must be an odd prime.
    """
    try:
        p = int(witness)
        mod8 = p % 8
        
        # The conclusion states the value of the Legendre symbol based on p mod 8.
        # If p is not an odd prime, sympy.ntheory.legendre_symbol will raise a ValueError,
        # meaning the conclusion "The Legendre symbol is X" fails (is undefined).
        if mod8 in (1, 3):
            val = sympy.ntheory.legendre_symbol(-2, p)
            q_ok = (val == 1)
        elif mod8 in (5, 7):
            val = sympy.ntheory.legendre_symbol(-2, p)
            q_ok = (val == -1)
        else:
            # If p is not 1, 3, 5, or 7 mod 8, the implication is vacuously true.
            q_ok = True
            
    except Exception:
        # If evaluating the Legendre symbol fails (e.g., p is composite, even, or negative),
        # the conclusion fails to hold.
        q_ok = False

    neg_q = not q_ok
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Legendre symbol (-2/p) does not match the formula or is undefined"
]

N_HYP = 0
NEG_Q_INDEX = 0