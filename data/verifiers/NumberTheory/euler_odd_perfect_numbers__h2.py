import sympy

def conditions(witness):
    # H_1: N is an odd integer
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            h1 = (witness % 2 == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: N cannot be factored as p^\alpha m^2 with p \equiv \alpha \equiv 1 \pmod 4 and \gcd(p, m) = 1
    try:
        if not (isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool)):
            neg_q = False
        elif witness <= 0:
            # A non-positive integer cannot be factored into p^\alpha m^2 where p is a positive prime
            neg_q = True
        else:
            factors = sympy.factorint(witness)
            odd_exponent_primes = []
            for p, exp in factors.items():
                if exp % 2 == 1:
                    odd_exponent_primes.append((p, exp))
            
            # For N = p^\alpha m^2 with \gcd(p, m) = 1, p must be the ONLY prime with an odd exponent
            # (since \alpha \equiv 1 \pmod 4 implies \alpha is odd, and m^2 has only even exponents).
            if len(odd_exponent_primes) != 1:
                conclusion = False
            else:
                p, alpha = odd_exponent_primes[0]
                if p % 4 == 1 and alpha % 4 == 1:
                    conclusion = True
                else:
                    conclusion = False
            
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is an odd integer",
    "¬Q: N cannot be factored as p^\\alpha m^2 with p \\equiv \\alpha \\equiv 1 \\pmod 4 and \\gcd(p, m) = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1