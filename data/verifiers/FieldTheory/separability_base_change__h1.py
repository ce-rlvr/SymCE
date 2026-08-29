import sympy as sp

CONDITION_LABELS = [
    "H_1: E is a separable algebraic extension of F, and EK is the compositum of E and K",
    "¬Q: The compositum field EK is NOT a separable algebraic extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1

# Top-level setup: symbols that the witness expression may reference
u, E_var, K_var, EK_var = sp.symbols('u E_var K_var EK_var')

def is_zero_mod_p(expr, p, vars_list):
    """Check if a rational function is identically zero modulo p."""
    try:
        expr = sp.cancel(expr)
        num, den = expr.as_numer_denom()
        if num == 0:
            return True
        poly = sp.Poly(num, *vars_list, domain=sp.GF(p))
        return poly.is_zero
    except Exception:
        return False

def is_non_constant_mod_p(expr, p, var):
    """Check if a rational function is non-constant modulo p."""
    try:
        expr = sp.cancel(expr)
        num, den = expr.as_numer_denom()
        num_poly = sp.Poly(num, var, domain=sp.GF(p))
        den_poly = sp.Poly(den, var, domain=sp.GF(p))
        if den_poly.is_zero:
            return False
        gcd = num_poly.gcd(den_poly)
        num_poly = num_poly.exquo(gcd)
        den_poly = den_poly.exquo(gcd)
        return num_poly.degree() > 0 or den_poly.degree() > 0
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the witness against the remaining hypotheses and the negated conclusion.
    The witness should be a dictionary defining subfields of F_p(u) via rational functions.
    """
    try:
        p = witness['p']
        if not sp.isprime(p):
            h1 = False
        else:
            u_sym = witness['u']
            E_var_sym = witness['E_var']
            K_var_sym = witness['K_var']
            EK_var_sym = witness['EK_var']
            
            E_val = witness['E_val']
            F_val = witness['F_val']
            K_val = witness['K_val']
            EK_val = witness['EK_val']
            
            F_in_E = witness['F_in_E']
            E_in_EK = witness['E_in_EK']
            K_in_EK = witness['K_in_EK']
            EK_in_E_K = witness['EK_in_E_K']
            
            h1 = True
            
            # Check that all fields are non-constant (hence finite algebraic extensions of each other)
            for val in [E_val, F_val, K_val, EK_val]:
                if not is_non_constant_mod_p(val, p, u_sym):
                    h1 = False
                    break
                    
            if h1:
                # Check F is a subfield of E
                if not is_zero_mod_p(F_in_E.subs(E_var_sym, E_val) - F_val, p, [u_sym]):
                    h1 = False
                    
                # Check E is separable over F (derivative of the rational function must be non-zero mod p)
                elif is_zero_mod_p(sp.diff(F_in_E, E_var_sym), p, [E_var_sym]):
                    h1 = False
                    
                # Check EK is exactly the compositum of E and K
                elif not is_zero_mod_p(E_in_EK.subs(EK_var_sym, EK_val) - E_val, p, [u_sym]):
                    h1 = False
                elif not is_zero_mod_p(K_in_EK.subs(EK_var_sym, EK_val) - K_val, p, [u_sym]):
                    h1 = False
                elif not is_zero_mod_p(EK_in_E_K.subs({E_var_sym: E_val, K_var_sym: K_val}) - EK_val, p, [u_sym]):
                    h1 = False
    except Exception:
        h1 = False

    try:
        p = witness['p']
        EK_var_sym = witness['EK_var']
        K_in_EK = witness['K_in_EK']
        
        # EK is inseparable over K iff the derivative of the rational function expressing K in terms of EK is zero mod p
        neg_q = is_zero_mod_p(sp.diff(K_in_EK, EK_var_sym), p, [EK_var_sym])
    except Exception:
        neg_q = False

    return [h1, neg_q]