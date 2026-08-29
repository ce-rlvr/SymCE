import math
import sympy
from sympy.abc import x, y, z
from sympy import Rational, Integer

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a nilpotent ideal of R",
    "¬Q: There does not exist an idempotent e in R such that e + I = e_bar"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('R', 0))
            I_gen = witness.get('I_gen', witness.get('I', 0))
            e_bar_rep = witness.get('e_bar_rep', witness.get('e_bar', 0))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, I_gen, e_bar_rep = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        n = int(n)
        if n > 10000:
            return [False, False, False]
            
        if isinstance(I_gen, (list, tuple)):
            I_gen_val = 0
            for gen in I_gen:
                I_gen_val = math.gcd(I_gen_val, int(gen))
            I_gen = I_gen_val
        else:
            I_gen = int(I_gen)
            
        e_bar_rep = int(e_bar_rep)
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = (n >= 2)
    except Exception:
        h1 = False

    # H_2: I is a nilpotent ideal of R
    try:
        if not h1:
            h2 = False
        else:
            is_nilpotent = False
            val = I_gen % n
            for _ in range(n + 1):
                if val == 0:
                    is_nilpotent = True
                    break
                val = (val * I_gen) % n
            h2 = is_nilpotent
    except Exception:
        h2 = False

    # ¬Q: There does not exist an idempotent e in R such that e + I = e_bar
    try:
        if not h1:
            neg_q = False
        else:
            ideal_gen = math.gcd(I_gen, n)
            exists_lift = False
            for e in range(n):
                if (e * e) % n == e:  # e is idempotent
                    if (e - e_bar_rep) % ideal_gen == 0:
                        exists_lift = True
                        break
            neg_q = not exists_lift
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]