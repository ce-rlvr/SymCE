import sympy
import sympy.ntheory
import math

# Top-level setup
# No specific named bindings needed for Number Theory

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion.
    """
    # Extract x and n from the witness
    if isinstance(witness, dict):
        x = witness.get('x')
        n = witness.get('n')
    elif hasattr(witness, 'x') and hasattr(witness, 'n'):
        x = witness.x
        n = witness.n
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        x, n = witness[0], witness[1]
    else:
        # If only a single value is provided, assume it represents both x and n
        # to test if it triggers the counterexample edge cases (e.g., n=0).
        x = witness
        n = witness

    # H_1: x is an integer
    try:
        h1 = (isinstance(x, int) or isinstance(x, sympy.Integer)) and not isinstance(x, bool)
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails
    try:
        if n is None:
            neg_q = False
        elif not (isinstance(n, int) or isinstance(n, sympy.Integer)) or isinstance(n, bool):
            # If n is not an integer, the ring Z/nZ is invalid, so the conclusion fails.
            neg_q = True
        elif int(n) in (0, 1, -1):
            # For n=0, the radical p_1...p_r is undefined.
            # For n=1 or -1, the product of prime factors is empty, violating the p_1...p_r form.
            neg_q = True
        else:
            n_val = int(n)
            x_val = int(x)
            
            # Evaluate RHS: x is a multiple of the radical p_1 p_2 ... p_r
            factors = sympy.ntheory.primefactors(abs(n_val))
            rad = 1
            for p in factors:
                rad *= p
            rhs = (x_val % rad == 0)
            
            # Evaluate LHS: x is nilpotent in Z/nZ
            lhs = False
            curr = x_val % n_val
            # The nilpotency index is bounded by max(a_i) <= log2(n)
            max_k = int(math.log2(abs(n_val))) + 2
            for _ in range(max_k):
                if curr == 0:
                    lhs = True
                    break
                curr = (curr * x_val) % n_val
                
            # The conclusion fails if LHS and RHS are not equivalent
            neg_q = (lhs != rhs)
    except Exception:
        # If evaluation fails (e.g., undefined operations), the conclusion fails
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an integer",
    "¬Q: The residue class of x is nilpotent mod n iff x is a multiple of the radical fails"
]

N_HYP = 1
NEG_Q_INDEX = 1