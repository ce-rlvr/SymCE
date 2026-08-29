import sympy

# Top-level setup
# (No special objects needed for integer witnesses in this domain)

def conditions(witness):
    """
    Checks whether the given witness satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    # H_1: A regular n-gon is constructible using only an unmarked straightedge and a compass
    try:
        w = sympy.sympify(witness)
        if not w.is_integer:
            h1 = False
        else:
            n = int(w)
            # A regular n-gon is constructible iff n >= 3 and n is the product of 
            # a power of 2 and any number of distinct Fermat primes.
            if n < 3:
                h1 = False
            else:
                factors = sympy.factorint(n)
                h1 = True
                for p, mult in factors.items():
                    if p == 2:
                        continue
                    if mult > 1:
                        h1 = False
                        break
                    # Check if p is a Fermat prime (i.e., p-1 is a power of 2)
                    if (p - 1) & (p - 2) != 0:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # Q: The Euler totient function \phi(n) is a power of 2
    try:
        w = sympy.sympify(witness)
        if not w.is_integer:
            q = False
        else:
            n = int(w)
            if n <= 0:
                q = False
            else:
                phi = int(sympy.totient(n))
                # Check if phi is a power of 2
                q = (phi & (phi - 1)) == 0 and phi > 0
    except Exception:
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A regular n-gon is constructible using only an unmarked straightedge and a compass",
    "¬Q: The Euler totient function phi(n) is not a power of 2"
]

N_HYP = 1
NEG_Q_INDEX = 1