import math

CONDITION_LABELS = [
    "¬Q: (∃ x, y ∈ ℤ, p = x² + 2y²) ⟷ (p ≡ 1 or 3 mod 8) is FALSE"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        p = int(witness)
        
        has_solution = False
        if p >= 0:
            for y in range(math.isqrt(p // 2) + 1):
                rem = p - 2 * y**2
                if rem >= 0:
                    x = math.isqrt(rem)
                    if x * x == rem:
                        has_solution = True
                        break
                        
        mod_condition = (p % 8 == 1) or (p % 8 == 3)
        
        neg_q = (has_solution != mod_condition)
        
        return [bool(neg_q)]
    except Exception:
        return [False]