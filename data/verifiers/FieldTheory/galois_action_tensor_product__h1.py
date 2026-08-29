import sympy
from sympy import Poly, Symbol, RootOf, factor_list
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness (a polynomial representing the field extension E = QQ[x]/(witness) over F = QQ)
    makes the conclusion fail.
    
    The conclusion states that the E-algebra homomorphism from E \otimes_F E to \prod_{\sigma \in G} E 
    is an isomorphism. This holds if and only if E/F is a Galois extension, which means the degree of 
    the extension equals the size of the Galois group Aut(E/F).
    """
    try:
        syms = list(witness.free_symbols)
        if len(syms) != 1:
            return [False]
        var = syms[0]
        
        # The witness must be an irreducible polynomial over QQ to define a valid field extension E.
        p = Poly(witness, var, domain='QQ')
        if not p.is_irreducible:
            return [False]
            
        deg = p.degree()
        
        # To find the size of the Galois group G = Aut(E/F), we count the number
        # of roots of the polynomial in the extension field E.
        # This is equivalent to the number of linear factors of p(y) over E.
        y_var = Symbol('y_var')
        p_y = p.as_expr().subs(var, y_var)
        r = RootOf(p.as_expr(), 0)
        
        factors = factor_list(p_y, extension=r)
        
        num_roots = 0
        for factor, mult in factors[1]:
            if Poly(factor, y_var).degree() == 1:
                num_roots += mult
                
        # The map is an isomorphism iff dim_E(E \otimes_F E) == dim_E(\prod_{\sigma \in G} E)
        # dim_E(E \otimes_F E) = [E:F] = deg
        # dim_E(\prod_{\sigma \in G} E) = |G| = num_roots
        is_iso = (deg == num_roots)
        
        neg_Q = not is_iso
        
        return [bool(neg_Q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The E-algebra homomorphism is not an isomorphism (E/F is not Galois)"
]

N_HYP = 0
NEG_Q_INDEX = 0