import sympy
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            return [False]
        n = int(witness)
        if n != witness:
            return [False]
    except Exception:
        return [False]

    try:
        if n < 0:
            num_solutions = 0
        elif n == 0:
            num_solutions = 1
        else:
            if n > 10**12:
                return [False]
            num_solutions = 0
            limit = math.isqrt(n)
            for x in range(-limit, limit + 1):
                y2 = n - x**2
                if y2 < 0:
                    continue
                y = math.isqrt(y2)
                if y**2 == y2:
                    if y == 0:
                        num_solutions += 1
                    else:
                        num_solutions += 2
                        
        if n == 0:
            formula_val = None
        else:
            divs = sympy.divisors(abs(n))
            d1 = sum(1 for d in divs if d % 4 == 1)
            d3 = sum(1 for d in divs if d % 4 == 3)
            formula_val = 4 * (d1 - d3)
            
        neg_q = (formula_val != num_solutions)
    except Exception:
        neg_q = True

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The number of solutions to x^2 + y^2 = n is not exactly 4(d_1(n) - d_3(n))"
]

N_HYP = 0
NEG_Q_INDEX = 0