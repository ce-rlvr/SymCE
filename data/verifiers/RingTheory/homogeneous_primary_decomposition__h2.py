import sympy
from sympy import groebner, Poly
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a list of generators for an ideal I in a polynomial ring,
    or a tuple (variables, generators).
    """
    try:
        # Parse the witness into variables and generators
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple, set)):
            vars, gens = witness
        elif hasattr(witness, 'gens'):
            gens = witness.gens
            vars = list(set().union(*[getattr(g, 'free_symbols', set()) for g in gens]))
            vars = sorted(vars, key=lambda sym: sym.name)
        else:
            gens = witness
            if not isinstance(gens, (list, tuple, set)):
                gens = [gens]
            vars = list(set().union(*[getattr(g, 'free_symbols', set()) for g in gens]))
            vars = sorted(vars, key=lambda sym: sym.name)
            
        if not vars:
            vars = [sympy.Symbol('x')]
            
        if not gens:
            # The zero ideal is homogeneous, so it admits a homogeneous primary decomposition.
            return [True, True, False]
            
        # H_1: R is a graded commutative ring.
        # A polynomial ring over a field is a graded commutative ring.
        h1 = True
        
        # H_2: I admits a primary decomposition.
        # A polynomial ring over a field is Noetherian, so every ideal admits a primary decomposition.
        h2 = True
        
        # ¬Q: I does NOT admit a primary decomposition where every primary component is a homogeneous ideal.
        # Since the intersection of homogeneous ideals is homogeneous, I admits such a decomposition
        # if and only if I itself is a homogeneous ideal.
        # Thus, ¬Q is True if and only if I is NOT a homogeneous ideal.
        # We check this by computing the reduced Groebner basis; an ideal is homogeneous iff 
        # its reduced Groebner basis consists entirely of homogeneous polynomials.
        gb = groebner(gens, *vars)
        
        is_homog_ideal = True
        for p_expr in gb:
            p = Poly(p_expr, *vars)
            if p.is_zero:
                continue
            # Calculate the total degree of each monomial
            degrees = [sum(monom) for monom in p.monoms()]
            if len(set(degrees)) > 1:
                is_homog_ideal = False
                break
                
        neg_q = not is_homog_ideal
        
        return [h1, h2, neg_q]
    except Exception:
        # If any computation fails (e.g., non-polynomial expressions), it's an invalid witness.
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a graded commutative ring",
    "H_2: I admits a primary decomposition",
    "¬Q: I does not admit a primary decomposition where every primary component is a homogeneous ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2