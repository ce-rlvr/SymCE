import sympy
from sympy import Poly
from sympy.abc import x, y, z

QQ = sympy.QQ
ZZ = sympy.ZZ

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over a field R",
    "H_2: f(x) has degree > 1",
    "H_3: f(x) is irreducible over R",
    "H_4: E is the splitting field of f(x) over R",
    "¬Q: The degree of f(x) is not 2, or E is not isomorphic to R(\\sqrt{-1})"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if not isinstance(witness, Poly):
            witness = Poly(witness)
        if witness.domain == sympy.ZZ:
            witness = witness.set_domain(sympy.QQ)
    except Exception:
        return [False, False, False, False, False]
        
    try:
        if not witness.is_univariate:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H1: f(x) is a polynomial over a field R
    try:
        domain = witness.domain
        h1 = domain.is_Field
    except Exception:
        h1 = False
        
    # H2: degree > 1
    try:
        h2 = witness.degree() > 1
    except Exception:
        h2 = False
        
    # H3: irreducible
    try:
        h3 = witness.is_irreducible
    except Exception:
        h3 = False
        
    # H4: E is the splitting field of f(x) over R (true by definition for any f)
    h4 = True
    
    # neg_Q: degree != 2 OR E is not isomorphic to R(\sqrt{-1})
    try:
        if witness.degree() != 2:
            neg_q = True
        else:
            char = domain.characteristic
            if char == 2:
                neg_q = True
            else:
                gen = witness.gen
                a = witness.coeff_monomial(gen**2)
                b = witness.coeff_monomial(gen)
                c = witness.coeff_monomial(1)
                D = b**2 - 4*a*c
                test_poly = Poly(gen**2 + D, gen, domain=domain)
                neg_q = test_poly.is_irreducible
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]