import sympy
import math

# Top-level setup
# (No specific named objects needed for this number theory conjecture)

def conditions(witness):
    # Extract p, k, a from the witness
    try:
        if isinstance(witness, dict):
            p = int(witness['p'])
            k = int(witness['k'])
            a = int(witness.get('a', 0))
        elif isinstance(witness, (tuple, list)):
            p = int(witness[0])
            k = int(witness[1])
            a = int(witness[2]) if len(witness) > 2 else 0
        else:
            p, k, a = None, None, None
    except Exception:
        p, k, a = None, None, None

    # H_1: p is an odd prime number
    try:
        h1 = sympy.isprime(p) and p % 2 == 1
    except Exception:
        h1 = False

    # H_2: k is a positive integer
    try:
        h2 = k > 0
    except Exception:
        h2 = False

    # ¬Q: The equivalence between a being a k-th power mod p and its multiplicative order dividing (p-1)/gcd(k, p-1) fails
    try:
        if p is None or k is None or not h1 or not h2:
            neg_Q = False
        else:
            a_mod_p = a % p
            
            # Check if a is a k-th power modulo p
            if a_mod_p == 0:
                is_kth_power = True
            else:
                if p < 10000:
                    is_kth_power = False
                    for x in range(p):
                        if pow(x, k, p) == a_mod_p:
                            is_kth_power = True
                            break
                else:
                    # For large primes and a != 0, use Euler's criterion
                    target_power = (p - 1) // math.gcd(k, p - 1)
                    is_kth_power = (pow(a_mod_p, target_power, p) == 1)

            # Check if the multiplicative order of a modulo p divides (p-1)/gcd(k, p-1)
            if math.gcd(a, p) == 1:
                ord_a = sympy.n_order(a_mod_p, p)
                target_div = (p - 1) // math.gcd(k, p - 1)
                order_divides = (target_div % ord_a == 0)
            else:
                # If gcd(a, p) != 1, the multiplicative order is undefined, so the condition fails
                order_divides = False
                
            # The conclusion is an iff statement; it fails if the two sides have different truth values
            Q = (is_kth_power == order_divides)
            neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: k is a positive integer",
    "¬Q: The equivalence between a being a k-th power mod p and its multiplicative order dividing (p-1)/gcd(k, p-1) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2