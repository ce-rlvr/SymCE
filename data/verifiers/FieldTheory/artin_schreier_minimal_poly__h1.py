import sympy as sp

# Top-level setup
x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Given a witness (p, a), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the Artin-Schreier minimal polynomial conjecture.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
        else:
            p, a = witness[:2]
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(sp.isprime(p))
    except Exception:
        h1 = False
        
    # H_2: x^p - x - a has no roots in F (using F=Q)
    try:
        a_rat = sp.Rational(a)
        poly = x**p - x - a_rat
        rts = sp.roots(poly, x, domain='QQ')
        h2 = len(rts) == 0
    except Exception:
        h2 = False
        
    # neg_Q: x^p - x - a is not the minimal polynomial of alpha over F
    # This is equivalent to x^p - x - a being reducible over Q.
    try:
        a_rat = sp.Rational(a)
        poly = x**p - x - a_rat
        facs = sp.factor_list(poly, domain='QQ')
        # A polynomial is irreducible if it has exactly one factor with multiplicity 1
        is_irreducible = (len(facs[1]) == 1) and (facs[1][0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: x^p - x - a has no roots in F (using F=Q)",
    "¬Q: x^p - x - a is not the minimal polynomial of α over F (i.e. it is reducible over Q)"
]

N_HYP = 2
NEG_Q_INDEX = 2