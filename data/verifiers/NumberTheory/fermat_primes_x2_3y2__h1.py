import math

# Top-level setup
# (No named bindings needed for this number theory conjecture; integers are used directly)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        # Ensure the witness is exactly an integer (reject floats like 2.5 or strings)
        if p != witness:
            return [False]
        
        # Check if p can be written as x^2 + 3y^2
        has_rep = False
        if p >= 0:
            max_y = math.isqrt(p // 3)
            for y in range(max_y + 1):
                rem = p - 3 * y * y
                if rem >= 0:
                    x = math.isqrt(rem)
                    if x * x == rem:
                        has_rep = True
                        break
                        
        # Check if p = 3 or p ≡ 1 (mod 3)
        q_holds = (p == 3) or (p % 3 == 1)
        
        # The conclusion is the biconditional: has_rep <--> q_holds
        # The negation of the conclusion is that the biconditional is false (i.e., XOR)
        neg_q = (has_rep != q_holds)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: It is FALSE that (p can be written as x^2 + 3y^2 iff p = 3 or p ≡ 1 mod 3)"
]

N_HYP = 0
NEG_Q_INDEX = 0