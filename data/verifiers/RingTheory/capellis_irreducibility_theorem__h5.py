import sympy

# Top-level setup
QQ = sympy.QQ
ZZ = sympy.ZZ
x = sympy.Symbol('x')

def conditions(witness):
    """
    Given a witness (F, a, n), checks the hypotheses and negated conclusion
    for the false conjecture related to Capelli's Irreducibility Theorem.
    """
    try:
        F, a, n = witness
    except Exception:
        return [False] * 5

    # H_1: F is a field
    try:
        h1 = bool(hasattr(F, 'is_Field') and F.is_Field)
    except Exception:
        h1 = False

    # H_2: a is a non-zero element of F
    try:
        h2 = bool((a in F) and (a != F.zero))
    except Exception:
        h2 = False

    # H_3: n >= 2 is an integer
    try:
        h3 = bool(isinstance(n, (int, sympy.Integer)) and n >= 2)
    except Exception:
        h3 = False

    # H_4: For every prime p dividing n, there is no element b in F such that b^p = a
    # This is equivalent to saying x^p - a has no linear factors over F.
    try:
        h4 = True
        for p in sympy.primefactors(n):
            factors = sympy.factor_list(x**p - a, domain=F)[1]
            if any(f.degree() == 1 for f, mult in factors):
                h4 = False
                break
    except Exception:
        h4 = False

    # neg_Q: The polynomial x^n - a is NOT irreducible over F (i.e., it is reducible)
    try:
        factors = sympy.factor_list(x**n - a, domain=F)[1]
        # A polynomial of degree >= 2 is reducible if it factors into more than one 
        # irreducible polynomial (counting multiplicities).
        neg_q = bool(sum(mult for f, mult in factors) > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: a is a non-zero element of F",
    "H_3: n >= 2 is an integer",
    "H_4: For every prime p dividing n, a is not a p-th power in F",
    "¬Q: x^n - a is reducible over F"
]

N_HYP = 4
NEG_Q_INDEX = 4