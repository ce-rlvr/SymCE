import sympy
import math
from sympy import Integer, Rational

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness):
    try:
        # Witness is expected to be a tuple or list of three numbers: (n, a, k)
        if len(witness) != 3:
            return [False] * 5
        n, a, k = witness
    except Exception:
        return [False] * 5

    # H_1: n is an integer greater than or equal to 2
    try:
        h1 = (int(n) == n) and (n >= 2)
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = (int(a) == a)
    except Exception:
        h2 = False

    # H_3: k is strictly greater than 1
    try:
        h3 = (int(k) == k) and (k > 1)
    except Exception:
        h3 = False

    # H_4: The integer a - 1 is coprime to n
    try:
        h4 = math.gcd(int(a) - 1, int(n)) == 1
    except Exception:
        h4 = False

    # ¬Q: The sum \sum_{i=1}^{k} a^i is not congruent to 0 \pmod n
    try:
        n_int = int(n)
        a_int = int(a)
        k_int = int(k)
        
        if math.gcd(a_int - 1, n_int) == 1:
            # Using the geometric series formula modulo n
            inv = sympy.mod_inverse(a_int - 1, n_int)
            total_sum = (a_int * (pow(a_int, k_int, n_int) - 1) * inv) % n_int
        else:
            # Fallback for robustness if evaluated on non-coprime inputs
            if k_int > 100000:
                total_sum = 0 
            else:
                total_sum = sum(pow(a_int, i, n_int) for i in range(1, k_int + 1)) % n_int
                
        neg_q = (total_sum != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than or equal to 2",
    "H_2: a is an integer",
    "H_3: k is strictly greater than 1",
    "H_4: The integer a - 1 is coprime to n",
    "¬Q: The sum \\sum_{i=1}^{k} a^i is not congruent to 0 \\pmod n"
]

N_HYP = 4
NEG_Q_INDEX = 4