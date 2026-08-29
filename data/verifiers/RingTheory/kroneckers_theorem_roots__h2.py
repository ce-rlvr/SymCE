import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy import QQ, ZZ

# Standard algebra objects
Z2 = sympy.GF(2)
Z3 = sympy.GF(3)
Z5 = sympy.GF(5)

def check_neg_q(F, f):
    """
    Checks if there is NO extension field E of F containing a root of f.
    Returns True if no such extension exists (i.e., conclusion fails).
    """
    try:
        char_F = F.characteristic()
    except Exception:
        return False
        
    try:
        if isinstance(f, sympy.Poly):
            f_poly = f
        else:
            f_poly = sympy.Poly(f)
        char_f = f_poly.domain.characteristic()
    except Exception:
        char_f = 0
        
    if char_F == 0:
        # If F has characteristic 0, it embeds into an algebraically closed field of char 0.
        # Any polynomial of char > 0 cannot be mapped to it.
        if char_f > 0:
            return True
        else:
            return False
            
    else:
        p = char_F
        # If F has characteristic p > 0, it embeds into an algebraically closed field of char p.
        if char_f > 0 and char_f != p:
            return True
        if char_f == p:
            return False
            
        # If f has characteristic 0, we must reduce its coefficients modulo p.
        try:
            f_p = sympy.Poly(f_poly.as_expr(), *f_poly.gens, domain=sympy.GF(p))
            # If it reduces to a non-zero constant, it has no roots.
            return bool(f_p.degree() <= 0 and not f_p.is_zero)
        except Exception:
            # Fallback if SymPy's Poly conversion fails (e.g., due to algebraic numbers or division by p)
            is_non_zero_constant = True
            has_constant_term = False
            constant_is_zero = False
            
            # First pass: check for undefined coefficients (e.g., division by p)
            for powers, coeff in f_poly.terms():
                c_expr = sympy.sympify(coeff)
                num_coeff, rest = c_expr.as_coeff_Mul()
                if num_coeff.is_Rational:
                    if num_coeff.q % p == 0:
                        return True # Undefined coefficient, cannot be evaluated
                        
            # Second pass: check if the polynomial reduces to a non-zero constant mod p
            for powers, coeff in f_poly.terms():
                c_expr = sympy.sympify(coeff)
                num_coeff, rest = c_expr.as_coeff_Mul()
                if num_coeff.is_Rational:
                    rem = num_coeff.p % p
                    if rem == 0:
                        val = 0
                    else:
                        val = 1
                else:
                    val = 1 # Assume non-zero for unsimplifiable algebraic numbers
                    
                if sum(powers) > 0:
                    if val != 0:
                        is_non_zero_constant = False
                else:
                    has_constant_term = True
                    if val == 0:
                        constant_is_zero = True
                        
            if not is_non_zero_constant:
                return False
            if has_constant_term and not constant_is_zero:
                return True
            return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        F, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H_2: The degree of f(x) is strictly greater than 0
    try:
        if isinstance(f, sympy.Poly):
            deg = f.degree()
        else:
            deg = sympy.Poly(f).degree()
        h2 = bool(deg > 0)
    except Exception:
        h2 = False
        
    # ¬Q: There is NO extension field E of F containing an element alpha such that f(alpha) = 0
    try:
        neg_q = bool(check_neg_q(F, f))
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The degree of f(x) is strictly greater than 0",
    "¬Q: There is NO extension field E of F containing an element alpha such that f(alpha) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2