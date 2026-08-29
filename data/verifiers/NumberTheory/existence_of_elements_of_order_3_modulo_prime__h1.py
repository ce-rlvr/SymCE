import math

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p <= 1:
            return [False]
        
        has_order_3 = False
        for x in range(1, p):
            if math.gcd(x, p) == 1:
                if pow(x, 3, p) == 1 and x % p != 1:
                    has_order_3 = True
                    break
        
        p_mod_3_is_1 = (p % 3 == 1)
        
        neg_q = bool(has_order_3 != p_mod_3_is_1)
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: It is not true that an element of order 3 mod p exists iff p ≡ 1 mod 3"
]

N_HYP = 0
NEG_Q_INDEX = 0