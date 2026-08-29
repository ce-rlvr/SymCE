import sympy
from sympy import abc

# Top-level setup for witness evaluation
x = abc.x
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a polynomial expression in one variable, or a tuple (p, f(x)).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p_wit, f_wit = witness
        else:
            p_wit = None
            f_wit = witness

        # Parse the polynomial
        if isinstance(f_wit, sympy.Poly):
            f_expr = f_wit.as_expr()
            gen = f_wit.gen
        else:
            f_expr = sympy.sympify(f_wit)
            free_symbols = f_expr.free_symbols
            if len(free_symbols) != 1:
                return [False, False, False]
            gen = list(free_symbols)[0]
            
        f_poly = sympy.Poly(f_expr, gen, domain='QQ')
        p = f_poly.degree()
        
        # H_1: p is a prime number
        if p_wit is not None:
            h1_ok = sympy.isprime(p_wit) and (p_wit == p)
        else:
            h1_ok = sympy.isprime(p)
            
        # H_2: f(x) is an irreducible polynomial over Q
        h2_ok = f_poly.is_irreducible
        if h2_ok is None:
            h2_ok = False
            
        # ¬Q: The Galois group of f(x) over Q is NOT isomorphic to S_p
        neg_q_ok = False
        disc = sympy.discriminant(f_expr, gen)
        disc = sympy.S(disc)
        
        if disc.is_Rational:
            num = disc.p
            den = disc.q
            if sympy.is_perfect_square(num) and sympy.is_perfect_square(den):
                # If the discriminant is a perfect square in Q, the Galois group is a 
                # subgroup of the alternating group A_p. Since A_p is a proper subgroup 
                # of S_p (for p >= 2), the Galois group is definitely NOT S_p.
                neg_q_ok = True
            else:
                if p == 2 or p == 3:
                    # For p=2, the Galois group is always S2 (discriminant is never square).
                    # For p=3, if the discriminant is not a square, the Galois group is S3.
                    neg_q_ok = False
                else:
                    # For p > 3, if the discriminant is not a square, the Galois group 
                    # might or might not be S_p. We return False to avoid false positives,
                    # safely rejecting the witness if we cannot easily prove it's not S_p.
                    neg_q_ok = False
        else:
            neg_q_ok = False
            
    except Exception:
        return [False, False, False]
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: f(x) is an irreducible polynomial of degree p over Q",
    "¬Q: The Galois group of f(x) over Q is not isomorphic to S_p"
]

N_HYP = 2
NEG_Q_INDEX = 2