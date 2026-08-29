import sympy
import math

# Top-level setup
# (No specific named bindings required for this number theory problem)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
    except Exception:
        return [False, False]

    # H_1: p is an odd prime number
    try:
        h1_ok = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1_ok = False

    # ¬Q: The equivalence (p = x^2 + 7y^2 iff p ≡ 1, 2, 4 mod 7) fails
    try:
        if p < 0:
            exists_xy = False
        else:
            exists_xy = False
            max_y = math.isqrt(p // 7)
            for y in range(max_y + 1):
                rem = p - 7 * y**2
                if rem >= 0:
                    x = math.isqrt(rem)
                    if x**2 == rem:
                        exists_xy = True
                        break
        
        cond_mod = (p % 7) in [1, 2, 4]
        
        # Negated conclusion: the "if and only if" does not hold
        neg_q_ok = bool(exists_xy != cond_mod)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "¬Q: (exists x, y such that p = x^2 + 7y^2) is NOT equivalent to (p ≡ 1, 2, or 4 mod 7)"
]

N_HYP = 1
NEG_Q_INDEX = 1