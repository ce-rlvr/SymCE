import sympy
from sympy import symbols, QQ

# Top-level setup
# We define standard variables and a common polynomial ring that can be used as a witness.
# A valid counterexample is R = QQ[x, y] and I = (x, y).
x, y, z = symbols('x y z')
R_xy = QQ[x, y]

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture:
    "Every fractional ideal of an integral domain is principal."
    
    The witness should be a tuple (R, I_gens) where:
      - R is a SymPy polynomial ring over a field (e.g., QQ[x, y])
      - I_gens is a list of generators for the fractional ideal I (elements of R or its fraction field)
    """
    try:
        R, I_gens = witness
    except Exception:
        return [False, False, False]
        
    # H_1: K is the field of fractions of R (R is an integral domain)
    # For verification purposes, we restrict R to be a SymPy PolyRing over a field,
    # which guarantees it is an integral domain and allows Groebner basis computations.
    try:
        h1 = getattr(R, 'is_domain', False)
        if not isinstance(R, sympy.polys.rings.PolyRing):
            h1 = False
        elif not R.domain.is_Field:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: I is a fractional ideal of R in K
    # This means I is a finitely generated R-submodule of K.
    # We verify this by checking that I_gens is a non-empty list of elements in K.
    try:
        K = R.frac_field
        I_elements = []
        for expr in I_gens:
            try:
                elem = K(expr)
            except Exception:
                elem = K.from_expr(expr)
            I_elements.append(elem)
        h2 = len(I_elements) > 0
    except Exception:
        h2 = False
        
    # neg_Q: I is not a principal fractional ideal
    # A fractional ideal I is principal iff the corresponding integral ideal J = d*I is principal,
    # where d is a common denominator. J is principal iff its generators' GCD is in J.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            nums = [elem.numer for elem in I_elements]
            dens = [elem.denom for elem in I_elements]
            
            common_den = R.one
            for d in dens:
                common_den *= d
                
            J_gens = []
            for n, d in zip(nums, dens):
                quo, rem = divmod(common_den, d)
                if rem != 0:
                    raise ValueError("Division failed")
                J_gens.append(n * quo)
                
            J_gens = [f for f in J_gens if f != 0]
            
            if not J_gens:
                # The zero ideal is principal
                neg_q = False
            else:
                expr_gens = [f.as_expr() for f in J_gens]
                
                # Compute the GCD of the generators of J
                g_expr = expr_gens[0]
                for f_expr in expr_gens[1:]:
                    g_expr = sympy.gcd(g_expr, f_expr)
                    
                # Check if the GCD is in the ideal J using Groebner bases
                gens = R.gens
                G = sympy.groebner(expr_gens, *gens, domain=R.domain)
                Q, rem = sympy.reduced(g_expr, G, *gens, domain=R.domain)
                
                # If the remainder is non-zero, the GCD is not in J, so J (and I) is not principal
                neg_q = (sympy.expand(rem) != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R (R is an integral domain)",
    "H_2: I is a fractional ideal of R in K",
    "¬Q: I is not a principal fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2