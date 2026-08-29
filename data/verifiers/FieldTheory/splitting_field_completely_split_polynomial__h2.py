import sympy
from sympy import Poly, Symbol
from sympy.polys.domains import QQ, RR, CC, ZZ

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (F, K, f)
    where F and K are sympy domains (e.g., QQ) or strings representing fields,
    and f is a sympy expression representing the polynomial f(x).
    """
    try:
        F, K, f = witness
    except Exception:
        return [False, False, False]
        
    # H1: F is a field
    try:
        if hasattr(F, 'is_Field'):
            h1 = bool(F.is_Field)
        elif isinstance(F, str) and F in ['Q', 'R', 'C', 'QQ', 'RR', 'CC']:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: K is the splitting field of f over F
    try:
        domain_kwarg = F if isinstance(F, str) and F in ['QQ', 'RR', 'CC'] else None
        if domain_kwarg:
            f_poly = Poly(f, x, domain=domain_kwarg)
        else:
            f_poly = Poly(f, x)
            
        is_const = f_poly.is_zero or f_poly.degree() <= 0
        
        if is_const:
            # The splitting field of a constant polynomial over F is F itself.
            h2 = (K == F)
        else:
            # For non-constant polynomials, we do a basic check.
            # (Note: any valid counterexample to this specific theorem must be a constant polynomial,
            # so rejecting complex valid splitting fields for deg > 0 is safe as they wouldn't trigger neg_Q anyway).
            if K == F:
                factors = f_poly.factor_list()[1]
                h2 = all(fac.degree() == 1 for fac, mult in factors)
            else:
                h2 = False
    except Exception:
        h2 = False
        
    # Conclusion: K = F if and only if f(x) factors completely into a product of linear polynomials in F[x]
    try:
        k_eq_f = (K == F)
        
        if is_const:
            # A constant polynomial (degree <= 0) does not factor into a product of linear polynomials
            # (assuming the standard definition where a product of linear polynomials has degree >= 1).
            factors_completely = False
        else:
            factors = f_poly.factor_list()[1]
            factors_completely = all(fac.degree() == 1 for fac, mult in factors)
            
        conclusion = (k_eq_f == factors_completely)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: The equivalence (K = F iff f(x) factors completely into linear polynomials) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2