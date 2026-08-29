import sympy as sp
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "Let R be a UFD and R_x be the polynomial ring over R. 
    c is an irreducible element in R_x if and only if c is an irreducible element in R."
    
    The witness is expected to be a polynomial expression in one variable (e.g., x).
    We implicitly use R = ZZ or R = QQ based on the coefficients of the witness.
    """
    try:
        c = sp.sympify(witness)
    except Exception:
        return [False, False, False]
    
    # H_1: R is a unique factorization domain.
    # We restrict our check to ZZ or QQ, both of which are UFDs.
    h1 = True
    
    # H_2: R_x is the polynomial ring over R, and c is in R_x.
    try:
        free_syms = c.free_symbols
        if len(free_syms) > 1:
            h2 = False
            var = x
        elif len(free_syms) == 1:
            var = list(free_syms)[0]
        else:
            var = x
            
        if len(free_syms) <= 1:
            if not c.is_polynomial(var):
                h2 = False
            else:
                p = sp.Poly(c, var)
                coeffs = p.coeffs()
                if all(coeff.is_integer for coeff in coeffs):
                    domain = 'ZZ'
                    h2 = True
                elif all(coeff.is_rational for coeff in coeffs):
                    domain = 'QQ'
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # Conclusion: c is irreducible in R_x iff c is irreducible in R.
    try:
        if not h2:
            neg_q = False
        else:
            p = sp.Poly(c, var, domain=domain)
            if domain == 'ZZ':
                if p.degree() <= 0:
                    if p.is_zero:
                        irr_Rx = False
                        irr_R = False
                    else:
                        val = abs(p.coeffs()[0])
                        irr_Rx = sp.isprime(val)
                        irr_R = sp.isprime(val)
                else:
                    if p.content() != 1:
                        irr_Rx = False
                    else:
                        const, factors = sp.factor_list(c, domain='ZZ')
                        if abs(const) != 1:
                            irr_Rx = False
                        elif len(factors) == 1 and factors[0][1] == 1:
                            irr_Rx = True
                        else:
                            irr_Rx = False
                    irr_R = False
            elif domain == 'QQ':
                if p.degree() <= 0:
                    irr_Rx = False
                    irr_R = False
                else:
                    const, factors = sp.factor_list(c, domain='QQ')
                    if len(factors) == 1 and factors[0][1] == 1:
                        irr_Rx = True
                    else:
                        irr_Rx = False
                    irr_R = False
            
            neg_q = (irr_Rx != irr_R)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: c is in the polynomial ring over R",
    "¬Q: c is irreducible in the polynomial ring iff c is irreducible in R fails"
]

N_HYP = 2
NEG_Q_INDEX = 2