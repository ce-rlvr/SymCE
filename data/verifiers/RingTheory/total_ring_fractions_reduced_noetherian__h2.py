import sympy
from sympy import QQ, ZZ, symbols
from sympy.polys.polytools import groebner, reduced, Poly

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be a tuple representing a quotient ring:
      (domain, vars, ideal_gens) 
    or 
      (domain, vars, ideal_gens, nilpotent_element)
    where:
      - domain is QQ or ZZ
      - vars is a tuple of sympy symbols, e.g., (x,)
      - ideal_gens is a list of polynomials generating the ideal
      - nilpotent_element (optional) is an element in the ring that is nilpotent but not zero
    """
    h1 = False
    neg_q = False
    
    try:
        if len(witness) == 3:
            domain, vars, ideal_gens = witness
            nilpotent = None
        elif len(witness) == 4:
            domain, vars, ideal_gens, nilpotent = witness
        else:
            return [False, False]
            
        # Check H_1: R is a commutative Noetherian ring
        # A finitely generated algebra over QQ or ZZ is a commutative Noetherian ring.
        if domain in [QQ, ZZ] and isinstance(vars, tuple) and isinstance(ideal_gens, (list, tuple)):
            h1 = True
            for v in vars:
                if not isinstance(v, sympy.Symbol):
                    h1 = False
            for g in ideal_gens:
                if hasattr(g, 'free_symbols'):
                    if not g.free_symbols.issubset(set(vars)):
                        h1 = False
                elif not isinstance(g, (int, sympy.Integer, float, sympy.Float)):
                    h1 = False
                    
        # Check neg_Q: The total ring of fractions of R is NOT isomorphic to a finite direct product of fields.
        # For a Noetherian ring, its total ring of fractions is a finite direct product of fields 
        # if and only if the ring is reduced. Thus, we check if R has a non-zero nilpotent element.
        if h1:
            if nilpotent is not None:
                if ideal_gens:
                    G = groebner(ideal_gens, *vars, domain=domain)
                    rem1 = reduced(nilpotent, G, *vars, domain=domain)[1]
                else:
                    rem1 = nilpotent
                
                # Check if the element is non-zero in the quotient ring
                if rem1 != 0:
                    # Check if some power of the element is zero in the quotient ring
                    for k in range(2, 10):
                        if ideal_gens:
                            remk = reduced(nilpotent**k, G, *vars, domain=domain)[1]
                        else:
                            remk = nilpotent**k
                        if remk == 0:
                            neg_q = True
                            break
            else:
                # Fallback for univariate rings without an explicitly provided nilpotent element
                if len(vars) == 1 and ideal_gens:
                    v = vars[0]
                    f_poly = Poly(ideal_gens[0], v, domain=domain)
                    for g in ideal_gens[1:]:
                        f_poly = f_poly.gcd(Poly(g, v, domain=domain))
                    
                    if not f_poly.is_zero:
                        f_diff = f_poly.diff(v)
                        g_gcd = f_poly.gcd(f_diff)
                        # If the generator shares a factor with its derivative, it has multiple roots,
                        # meaning the quotient ring contains nilpotents.
                        if g_gcd.degree() > 0:
                            neg_q = True

    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The total ring of fractions of R is not isomorphic to a finite direct product of fields"
]

N_HYP = 1
NEG_Q_INDEX = 1