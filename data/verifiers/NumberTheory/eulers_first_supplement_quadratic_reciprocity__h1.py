import sympy
from sympy.ntheory import factorint

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        h1 = (p > 2)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p <= 0:
            neg_q = False
        else:
            # Check if there exists x such that x^2 == -1 mod p
            # By the Chinese Remainder Theorem and Hensel's Lemma, x^2 == -1 mod p
            # has a solution if and only if p is not divisible by 4, and every
            # odd prime factor of p is congruent to 1 modulo 4.
            if p % 4 == 0:
                exists_x = False
            else:
                factors = factorint(p)
                exists_x = True
                for q in factors:
                    if q > 2 and q % 4 != 1:
                        exists_x = False
                        break
            
            p_mod_4_eq_1 = (p % 4 == 1)
            
            # The conclusion is that exists_x is equivalent to p_mod_4_eq_1.
            # The negated conclusion is that they are NOT equivalent.
            neg_q = (exists_x != p_mod_4_eq_1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p > 2",
    "¬Q: (exists x, x^2 == -1 mod p) is not equivalent to (p == 1 mod 4)"
]

N_HYP = 1
NEG_Q_INDEX = 1