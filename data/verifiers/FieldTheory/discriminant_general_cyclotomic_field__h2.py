import sympy

def conditions(witness):
    try:
        n = int(witness)
        h1 = (n > 2)
    except Exception:
        h1 = False

    try:
        # K = Q(zeta_n) is the n-th cyclotomic field
        # This is a definitional hypothesis, so it holds for any valid integer witness
        h2 = isinstance(n, int)
    except Exception:
        h2 = False

    try:
        # Evaluate the formula given in the conclusion
        phi_n = sympy.totient(n)
        sign = (-1)**(phi_n // 2)
        num = n**phi_n
        den = 1
        for p in sympy.primefactors(n):
            den *= p**(phi_n // (p - 1))
        formula_disc = sign * num // den
        
        # Compute the true discriminant of the field K = Q(zeta_n)
        # If n = 2 (mod 4), Q(zeta_n) = Q(zeta_{n/2}), so the true discriminant is that of n/2
        m = n // 2 if n % 4 == 2 else n
        phi_m = sympy.totient(m)
        sign_m = (-1)**(phi_m // 2)
        num_m = m**phi_m
        den_m = 1
        for p in sympy.primefactors(m):
            den_m *= p**(phi_m // (p - 1))
        true_disc = sign_m * num_m // den_m
        
        # The conclusion fails if the true discriminant is not equal to the formula
        neg_q = (true_disc != formula_disc)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "H_2: K = Q(zeta_n) is the n-th cyclotomic field",
    "¬Q: The discriminant of K over Q is not equal to the given formula"
]

N_HYP = 2
NEG_Q_INDEX = 2