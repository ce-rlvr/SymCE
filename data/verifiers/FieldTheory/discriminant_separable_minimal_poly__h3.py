import sympy as sp

# Top-level setup for potential witness expressions
x, t, y, z = sp.symbols('x t y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a SymPy Poly object representing the minimal polynomial m(x)
    over a field F, or a tuple (expr, var, domain).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                expr, var, domain = witness
                m = sp.Poly(expr, var, domain=domain)
            else:
                return [False, False, False, False]
        elif isinstance(witness, sp.Poly):
            m = witness
        else:
            return [False, False, False, False]
            
        # H1: F is a field and α is algebraic over F
        try:
            h1 = m.domain.is_Field
        except Exception:
            h1 = False
            
        # H2: m(x) is the minimal polynomial of α over F
        # This requires m(x) to be monic, non-constant, and irreducible over F.
        try:
            h2 = m.is_monic and m.degree() >= 1
            if h2:
                try:
                    irred = m.is_irreducible
                    if irred is None:
                        raise ValueError("Cannot determine irreducibility directly")
                    h2 = h2 and irred
                except Exception:
                    # Fallback for fraction fields (e.g., GF(p)(t)) where is_irreducible might fail
                    irred_fallback = False
                    try:
                        if hasattr(m.domain, 'ring') and hasattr(m.domain.ring, 'gens'):
                            gens = m.domain.ring.gens
                            base_domain = m.domain.ring.domain
                            all_gens = (m.gen,) + gens
                            expr = m.as_expr()
                            # Clear denominators to check irreducibility over the base polynomial ring
                            numer, denom = sp.cancel(expr).as_numer_denom()
                            poly_num = sp.Poly(numer, *all_gens, domain=base_domain)
                            irred_fallback = poly_num.is_irreducible
                            if irred_fallback is None:
                                irred_fallback = False
                    except Exception:
                        pass
                    h2 = h2 and irred_fallback
        except Exception:
            h2 = False
            
        # H3: Δ is the discriminant of m(x)
        try:
            # For an irreducible polynomial, the discriminant is 0 iff the derivative is the zero polynomial
            # (which happens in inseparable extensions). This avoids potential resultant bugs with 0.
            if m.diff().is_zero:
                delta = m.domain.zero
                h3 = True
            else:
                delta = m.discriminant()
                h3 = True
        except Exception:
            # Fallback manual discriminant for degree 2
            try:
                if m.degree() == 2:
                    coeffs = m.all_coeffs()
                    a, b, c = coeffs[0], coeffs[1], coeffs[2]
                    delta = b**2 - 4*a*c
                    h3 = True
                else:
                    h3 = False
            except Exception:
                h3 = False
                
        # ¬Q: The discriminant Δ is zero (negation of "Δ is a non-zero element of F")
        try:
            if h3:
                if isinstance(delta, sp.Expr):
                    neg_q = bool(sp.simplify(delta) == 0)
                elif hasattr(delta, 'is_zero') and delta.is_zero is not None:
                    neg_q = bool(delta.is_zero)
                else:
                    try:
                        neg_q = bool(delta == m.domain.zero)
                    except Exception:
                        neg_q = bool(delta == 0)
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field and α is algebraic over F",
    "H_2: m(x) is the minimal polynomial of α over F",
    "H_3: Δ is the discriminant of m(x)",
    "¬Q: Δ is zero"
]

N_HYP = 3
NEG_Q_INDEX = 3