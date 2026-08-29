import sympy
from sympy import Poly, Eq
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: X \\subseteq \\mathbb{A}^1(K) is an irreducible algebraic set in the Zariski topology",
    "¬Q: X is neither a single point nor the entire affine line \\mathbb{A}^1(K)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_poly(witness):
    """
    Helper function to extract a univariate polynomial from the witness.
    """
    if isinstance(witness, (list, tuple, set)):
        if len(witness) != 1:
            return None
        w = list(witness)[0]
    else:
        w = witness
        
    if hasattr(w, "lhs") and hasattr(w, "rhs"):
        w = w.lhs - w.rhs
        
    if isinstance(w, Poly):
        return w
        
    free = getattr(w, "free_symbols", set())
    if len(free) == 1:
        x_sym = list(free)[0]
        return Poly(w, x_sym)
    elif len(free) == 0:
        return Poly(w, x)
    else:
        return None

def conditions(witness):
    try:
        p = get_poly(witness)
        if p is None:
            h1 = False
        else:
            # To check irreducibility properly, we need to work over a field (e.g., QQ instead of ZZ)
            if not p.domain.is_Field:
                p_field = p.set_domain(p.domain.get_field())
            else:
                p_field = p
                
            # The zero ideal is prime, corresponding to the entire affine line (which is irreducible)
            if p_field.is_zero:
                h1 = True
            else:
                # An algebraic set is irreducible iff its defining ideal is prime.
                # In K[x], this means the polynomial is irreducible.
                h1 = p_field.is_irreducible
    except Exception:
        h1 = False
        
    try:
        p = get_poly(witness)
        if p is None:
            neg_q = False
        else:
            if p.is_zero:
                # The zero polynomial corresponds to the entire affine line, so the conclusion holds.
                neg_q = False
            else:
                # A single K-rational point corresponds to a polynomial of degree 1.
                # If degree > 1, it is a closed point of higher degree (neither a single point nor the whole line).
                neg_q = p.degree() > 1
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]