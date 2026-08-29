import math

CONDITION_LABELS = [
    "H_1: p is congruent to 1 modulo 4",
    "¬Q: The Diophantine equation x^2 - py^2 = -1 has no solution in integers x and y"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # H_1: p is congruent to 1 modulo 4
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            p = int(witness)
            h1 = (p == witness) and (p % 4 == 1)
    except Exception:
        h1 = False

    # ¬Q: The Diophantine equation x^2 - py^2 = -1 has no solution in integers x and y
    try:
        if not h1:
            neg_q = False
        else:
            p = int(witness)
            if p < 0:
                has_sol = False
            elif p == 0:
                has_sol = False
            else:
                r = math.isqrt(p)
                if r * r == p:
                    # The only perfect square p for which x^2 - p*y^2 = -1 has a solution is p = 1 (x=0, y=1)
                    has_sol = (p == 1)
                else:
                    # For non-square p, the negative Pell equation has a solution 
                    # iff the continued fraction expansion of sqrt(p) has an odd period length.
                    m = 0
                    d = 1
                    a = r
                    a0 = r
                    period = 0
                    while a != 2 * a0:
                        m = d * a - m
                        d = (p - m * m) // d
                        a = (a0 + m) // d
                        period += 1
                        if period > 1000000:
                            raise ValueError("Period too long")
                    has_sol = (period % 2 != 0)
            neg_q = not has_sol
    except Exception:
        neg_q = False

    return [h1, neg_q]