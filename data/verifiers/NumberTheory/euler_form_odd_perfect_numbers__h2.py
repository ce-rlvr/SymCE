import sympy
import sympy.ntheory

def conditions(witness):
    # H_1: n is an odd integer
    try:
        if isinstance(witness, bool):
            h1_ok = False
        elif isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1_ok = (n % 2 != 0)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: n cannot be written as p^k m^2 with p = 1 (mod 4), k = 1 (mod 4), and gcd(p, m) = 1
    try:
        if isinstance(witness, bool):
            q_ok = False
        elif isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n <= 0:
                q_ok = False
            else:
                factors = sympy.ntheory.factorint(n)
                odd_exp_primes = [p for p, exp in factors.items() if exp % 2 != 0]
                if len(odd_exp_primes) != 1:
                    q_ok = False
                else:
                    p = odd_exp_primes[0]
                    k = factors[p]
                    q_ok = (p % 4 == 1) and (k % 4 == 1)
        else:
            q_ok = False
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an odd integer",
    "¬Q: n cannot be written as p^k m^2 with p ≡ 1 (mod 4), k ≡ 1 (mod 4), and gcd(p, m) = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1