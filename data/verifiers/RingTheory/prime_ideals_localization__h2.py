import sympy

# Top-level setup for potential witness expressions
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary or tuple containing:
      - R: The ring (expected to be Z or equivalent)
      - P: The generator of the prime ideal (an integer)
      - S: A list or set of integers representing the subset S
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            P = witness.get('P')
            S = witness.get('S')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, P, S = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        R_str = str(R).strip()
        # We restrict verification to the integers for simplicity and robustness
        if R_str in ['Z', 'Integers', 'ZZ', 'S.Integers', 'IntegerRing()']:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: P is a prime ideal of R such that P \cap S = \emptyset
    try:
        P_val = int(P)
        if P_val == 0:
            is_prime = True
        else:
            is_prime = sympy.isprime(abs(P_val))
        
        S_vals = [int(s) for s in S]
        
        intersect_empty = True
        for s_val in S_vals:
            if P_val == 0:
                if s_val == 0:
                    intersect_empty = False
                    break
            else:
                if s_val % P_val == 0:
                    intersect_empty = False
                    break
        h2 = is_prime and intersect_empty
    except Exception:
        h2 = False

    # ¬Q: The extended ideal S^{-1}P is NOT a prime ideal in the localized ring S^{-1}R
    # This happens if S^{-1}R fails to be a ring (e.g., S is not multiplicatively closed).
    # In Z, the set of fractions F_S is a ring iff for all s1, s2 in S, 
    # 1/(s1*s2) and 1/s1 + 1/s2 can be written as r/s3 for some r in Z, s3 in S.
    try:
        is_ring = True
        if not S_vals:
            # If S is empty, S^{-1}R is empty, which is not a ring.
            is_ring = False
        else:
            for s1 in S_vals:
                for s2 in S_vals:
                    if s1 * s2 == 0:
                        is_ring = False
                        break
                    # Check closure under multiplication: 1/(s1*s2) in F_S
                    if not any(s3 % (s1 * s2) == 0 for s3 in S_vals):
                        is_ring = False
                        break
                    # Check closure under addition: 1/s1 + 1/s2 = (s1+s2)/(s1*s2) in F_S
                    if not any((s3 * (s1 + s2)) % (s1 * s2) == 0 for s3 in S_vals):
                        is_ring = False
                        break
                if not is_ring:
                    break
        neg_q = not is_ring
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal of R such that P \\cap S = \\emptyset",
    "¬Q: S^{-1}P is not a prime ideal in S^{-1}R (e.g., S^{-1}R is not a valid ring)"
]

N_HYP = 2
NEG_Q_INDEX = 2