import sympy
from sympy.ntheory import jacobi_symbol, totient

def conditions(witness):
    try:
        n = int(witness)
        if n < 2:
            return [False]
        
        if n % 2 == 0:
            count = 0
        else:
            count = 0
            power = (n - 1) // 2
            for a in range(1, n):
                if sympy.gcd(a, n) == 1:
                    lhs = pow(a, power, n)
                    rhs = jacobi_symbol(a, n) % n
                    if lhs == rhs:
                        count += 1
        
        phi_n = totient(n)
        neg_Q = bool(2 * count > phi_n)
    except Exception:
        neg_Q = False

    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The number of integers a coprime to n satisfying the congruence is > phi(n)/2"
]

N_HYP = 0
NEG_Q_INDEX = 0