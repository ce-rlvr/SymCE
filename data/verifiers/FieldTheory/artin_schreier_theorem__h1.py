import sympy
from sympy import Poly, Symbol, GF, QQ, ZZ

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false Artin-Schreier conjecture.
    The conjecture drops the hypothesis that the characteristic of K is p.
    A valid counterexample is typically a finite field extension where char(K) != p.
    Expected witness: a sympy.Poly object representing the minimal polynomial of the extension L/K.
    """
    try:
        if isinstance(witness, tuple):
            poly = witness[0]
        else:
            poly = witness
            
        if not isinstance(poly, sympy.Poly):
            poly = sympy.Poly(poly)
            
        p = poly.degree()
    except Exception:
        return [False, False, False, False]

    # H_1: Degree p of the extension is prime
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: Polynomial defining L/K is irreducible over K (so [L:K] = p)
    try:
        h2 = bool(poly.is_irreducible)
    except Exception:
        h2 = False

    # H_3: The extension L/K is cyclic Galois
    try:
        if poly.domain.is_FiniteField:
            # Any finite extension of a finite field is cyclic Galois
            h3 = True
        elif poly.domain == sympy.QQ:
            if p == 2:
                # Any quadratic extension is cyclic Galois
                h3 = True
            elif p == 3:
                # A cubic extension of QQ is Galois iff its discriminant is a perfect square
                disc = poly.discriminant()
                h3 = bool(sympy.sqrt(disc).is_rational)
            else:
                # For higher degrees over QQ, it's harder to check quickly; assume False
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The conclusion FAILS.
    # Conclusion: There exists alpha in L such that L = K(alpha) and alpha^p - alpha - a = 0 for some a in K.
    # This means x^p - x - a must have an irreducible factor of degree p over K.
    try:
        conclusion = False
        x_sym = sympy.Symbol('x')
        
        if poly.domain.is_FiniteField:
            q = int(poly.domain.order)
            if q > 1000:
                # Prevent timeouts for unreasonably large finite fields
                conclusion = True
            else:
                for a in range(q):
                    test_poly = sympy.Poly(x_sym**p - x_sym - a, domain=poly.domain)
                    factors = test_poly.factor_list()[1]
                    # If there is an irreducible factor of degree p, its roots generate L
                    if any(f.degree() == p for f, _ in factors):
                        conclusion = True
                        break
        elif poly.domain == sympy.QQ:
            # Over QQ, finding a counterexample is not the intended path and is hard to verify.
            # We assume the conclusion holds to reject the witness.
            conclusion = True
        else:
            conclusion = True
            
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Degree p of the extension is prime",
    "H_2: Polynomial defining L/K is irreducible over K",
    "H_3: The extension L/K is cyclic Galois",
    "¬Q: No element alpha in L generates L and satisfies alpha^p - alpha in K"
]

N_HYP = 3
NEG_Q_INDEX = 3