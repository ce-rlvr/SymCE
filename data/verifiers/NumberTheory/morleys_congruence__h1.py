import math
import sympy

# Top-level setup
# (No specific objects needed for this number theory conjecture)

def conditions(witness):
    try:
        p = int(witness)
        # Safeguard against excessively large inputs that might slow down math.comb
        if abs(p) > 10**6:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: p > 3
    try:
        h1_ok = bool(p > 3)
    except Exception:
        h1_ok = False
        
    # ¬Q: Conclusion fails
    try:
        if p % 2 != 0:
            k = (p - 1) // 2
            lhs = ((-1)**k) * math.comb(p - 1, k)
            mod = p**3
            lhs_mod = lhs % mod
            rhs_mod = pow(4, p - 1, mod)
            neg_q_ok = bool(lhs_mod != rhs_mod)
        else:
            # If p is even, the fractional exponent/binomial coefficient
            # means the congruence as stated for integers does not hold.
            neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p > 3",
    "¬Q: (-1)^((p-1)/2) * binom(p-1, (p-1)/2) is not congruent to 4^(p-1) (mod p^3)"
]

N_HYP = 1
NEG_Q_INDEX = 1