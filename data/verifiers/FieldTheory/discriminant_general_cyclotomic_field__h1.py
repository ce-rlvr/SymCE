import sympy as sp

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity",
    "H_2: K = Q(zeta_n) is the n-th cyclotomic field",
    "¬Q: The discriminant of K over Q is NOT equal to the given formula"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        n = int(witness)
        if n < 1:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # If n is a positive integer, the definitions of zeta_n and K are valid.
    h1_ok = True
    h2_ok = True
    
    try:
        # The true discriminant of the n-th cyclotomic field Q(zeta_n) over Q
        if n == 1 or n == 2:
            # For n=1 and n=2, Q(zeta_n) = Q, which has discriminant 1.
            true_disc = sp.Integer(1)
        else:
            # For n > 2, the discriminant is given by the standard formula.
            phi_n = sp.totient(n)
            sign = (-1)**(sp.Rational(phi_n, 2))
            num = n**phi_n
            den = 1
            for p in sp.primefactors(n):
                den *= p**(sp.Rational(phi_n, p - 1))
            true_disc = sign * num / den

        # The formula given in the conclusion of the conjecture
        phi_n = sp.totient(n)
        sign = (-1)**(sp.Rational(phi_n, 2))
        num = n**phi_n
        den = 1
        for p in sp.primefactors(n):
            den *= p**(sp.Rational(phi_n, p - 1))
        formula_val = sign * num / den
        
        # The conclusion states that true_disc == formula_val.
        # We want neg_Q to be True when the conclusion FAILS.
        diff = sp.simplify(true_disc - formula_val)
        neg_q_ok = bool(diff != 0)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]