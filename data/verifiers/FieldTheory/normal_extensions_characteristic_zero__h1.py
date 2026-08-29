import sympy
from sympy import Poly, GF, rem, diff, isprime, symbols, expand

# Top-level setup: named object bindings that the witness expression may reference.
X, Y, t = symbols('X Y t')

CONDITION_LABELS = [
    "H_1: L/K is a finite normal extension",
    "¬Q: L/K is not a Galois extension"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a dictionary representing a finite extension L/K where K = GF(p)(t).
    Expected keys:
      - 'p': a prime number (characteristic of the field)
      - 'P': an irreducible polynomial in X over GF(p)[t], monic in X, representing the minimal polynomial of L/K.
      - 'roots': a list of polynomials in X and t representing all roots of P in L = K[X]/(P).
      - 'X', 'Y', 't': (optional) SymPy symbols used in the expressions.
    """
    try:
        if not isinstance(witness, dict):
            return [False, False]
            
        p = witness.get('p')
        P = witness.get('P')
        roots = witness.get('roots')
        
        X_sym = witness.get('X', X)
        t_sym = witness.get('t', t)
        Y_sym = witness.get('Y', Y)
        
        if p is None or P is None or roots is None:
            return [False, False]
            
    except Exception:
        return [False, False]
        
    h1_ok = False
    try:
        if isprime(p):
            # Check P is a polynomial in X and t over GF(p)
            poly_P = Poly(P, X_sym, t_sym, domain=GF(p))
            d = poly_P.degree(X_sym)
            
            # The extension must be of degree >= 2 to be a proper extension
            if d >= 2:
                # Check that P is monic in X (leading term in X has no t and coefficient 1)
                lc_terms = [ (degs, c) for degs, c in poly_P.terms() if degs[0] == d ]
                if len(lc_terms) == 1 and lc_terms[0][0] == (d, 0) and lc_terms[0][1] == 1:
                    # Check irreducibility over GF(p)(t)
                    if poly_P.is_irreducible:
                        # Check that the number of provided roots matches the degree
                        if len(roots) == d:
                            prod = 1
                            for R in roots:
                                # Ensure R is a valid polynomial in X and t
                                Poly(R, X_sym, t_sym, domain=GF(p))
                                prod = prod * (Y_sym - R)
                                
                            # Check normality: P(Y) must split completely into \prod (Y - R) in L[Y]
                            # This is equivalent to \prod (Y - R) \equiv P(Y) \pmod{P(X)}
                            diff_expr = expand(prod - P.subs(X_sym, Y_sym))
                            remainder = rem(diff_expr, P, X_sym)
                            rem_poly = Poly(remainder, X_sym, Y_sym, t_sym, domain=GF(p))
                            
                            if rem_poly.is_zero:
                                h1_ok = True
    except Exception:
        h1_ok = False
        
    neg_q_ok = False
    try:
        if h1_ok:
            # L/K is Galois iff it is normal and separable.
            # Since H1 ensures it is normal, it is NOT Galois iff it is NOT separable.
            # An irreducible polynomial P is inseparable iff its formal derivative is 0.
            dP = diff(P, X_sym)
            dP_poly = Poly(dP, X_sym, t_sym, domain=GF(p))
            if dP_poly.is_zero:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]