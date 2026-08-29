import sympy
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for p != 3, x^2 + x + 1 is irreducible over F_p 
    if and only if p == 2 (mod 3).
    (The dropped hypothesis was that p is a prime).
    """
    try:
        w = sympy.sympify(witness)
        if w.is_integer is not True:
            return [False, False]
        p = int(w)
    except Exception:
        return [False, False]
        
    # Hypothesis 1: p != 3
    try:
        h1 = (p != 3)
    except Exception:
        h1 = False
        
    # Conclusion: x^2 + x + 1 is irreducible over F_p iff p = 2 (mod 3)
    # We interpret F_p as Z/pZ since p is not guaranteed to be prime.
    try:
        if p < 2:
            is_irred = False
        else:
            factors = sympy.factorint(p)
            # A monic quadratic is reducible over Z/pZ if p has >= 2 distinct prime factors.
            if len(factors) > 1:
                is_irred = False
            else:
                # p = q^k for some prime q
                q, k = list(factors.items())[0]
                if q % 3 == 1:
                    # Has roots mod q, which lift to roots mod q^k -> reducible
                    is_irred = False
                elif q % 3 == 2:
                    # Irreducible mod q, hence irreducible mod q^k
                    is_irred = True
                elif q == 3:
                    # For q=3, reducible mod 3, but strictly irreducible mod 3^k for k >= 2
                    is_irred = (k > 1)
                else:
                    is_irred = False
                    
        concl = (is_irred == (p % 3 == 2))
        neg_q = not concl
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p != 3",
    "¬Q: x^2 + x + 1 is irreducible over F_p iff p = 2 (mod 3) FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1