import sympy
from sympy import Poly, Symbol, QQ, ZZ

x = Symbol('x')

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (F, p, p_factors, f)
    where:
      F is a sympy Domain (e.g., QQ)
      p is a polynomial expression in x
      p_factors is a list of polynomial expressions in x
      f is a polynomial expression in x
    """
    try:
        F, p, p_factors, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    try:
        h1_ok = bool(hasattr(F, 'is_Field') and F.is_Field)
    except Exception:
        h1_ok = False
        
    # H_2: p_1(x), ..., p_k(x) are the distinct irreducible factors of p(x) in F[x]
    try:
        coeff, factors = sympy.factor_list(p, x, domain=F)
        expected_factors = [base for base, exp in factors]
        
        def make_monic(poly_expr):
            poly = Poly(poly_expr, x, domain=F)
            if poly.is_zero:
                return poly.as_expr()
            return poly.quo(Poly(poly.LC(), x, domain=F)).as_expr()
            
        expected_monic = {make_monic(fac) for fac in expected_factors}
        actual_monic = {make_monic(fac) for fac in p_factors}
        
        h2_ok = (expected_monic == actual_monic) and len(p_factors) == len(actual_monic)
    except Exception:
        h2_ok = False
        
    # H_3: f(x) \in F[x] is a polynomial
    try:
        f_poly = Poly(f, x, domain=F)
        h3_ok = True
    except Exception:
        h3_ok = False
        
    # ¬Q: The conclusion FAILS at the witness
    # Conclusion: f(x) + (p(x)) is nilpotent in F[x]/(p(x)) iff p_1(x)...p_k(x) divides f(x)
    try:
        p_poly = Poly(p, x, domain=F)
        f_poly_q = Poly(f, x, domain=F)
        
        # Check if f(x) + (p(x)) is nilpotent
        if p_poly.is_zero:
            is_nilpotent = f_poly_q.is_zero
        else:
            # If nilpotent, f^n \in (p) for some n. 
            # The maximum required power is the degree of p(x) (or 1 if degree is 0).
            n = max(1, p_poly.degree())
            res = Poly(1, x, domain=F)
            base = f_poly_q.rem(p_poly)
            for _ in range(n):
                res = (res * base).rem(p_poly)
            is_nilpotent = res.is_zero
            
        # Check if the product of p_factors divides f(x)
        P = Poly(1, x, domain=F)
        for fac in p_factors:
            P = P * Poly(fac, x, domain=F)
            
        if P.is_zero:
            P_divides_f = f_poly_q.is_zero
        else:
            P_divides_f = f_poly_q.rem(P).is_zero
            
        iff_holds = (is_nilpotent == P_divides_f)
        neg_q = not iff_holds
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p_1, ..., p_k are the distinct irreducible factors of p over F",
    "H_3: f is a polynomial over F",
    "not Q: The coset f + (p) is nilpotent iff the product p_1...p_k divides f FAILS"
]

N_HYP = 3
NEG_Q_INDEX = 3