import sympy
import math

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        
        conclusion_holds = True
        if p <= 0:
            conclusion_holds = False
        else:
            limit = (p - 1) // 2
            sum_inv = 0
            for x in range(1, limit + 1):
                if math.gcd(x, p) != 1:
                    conclusion_holds = False
                    break
                sum_inv = (sum_inv + sympy.mod_inverse(x, p)) % p
            
            if conclusion_holds:
                if p == 1:
                    # For p=1, sum is 0, q_1(2) = 0, 0 == 0 mod 1
                    pass
                elif pow(2, p - 1, p) != 1:
                    # q_p(2) is not an integer
                    conclusion_holds = False
                else:
                    # Compute q_p(2) mod p efficiently using Fermat quotient property
                    val = (pow(2, p - 1, p**2) - 1) // p
                    rhs = (-2 * val) % p
                    if sum_inv != rhs:
                        conclusion_holds = False
                        
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The sum of inverses of the first half of residues mod p is not congruent to -2 q_p(2) mod p"
]

N_HYP = 0
NEG_Q_INDEX = 0