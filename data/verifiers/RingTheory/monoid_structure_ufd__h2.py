import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects required for this domain, but we provide standard symbols and fields.

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    # H1: R is an integral domain
    try:
        h1 = bool(
            getattr(witness, 'is_domain', False) or 
            getattr(witness, 'is_IntegralDomain', False) or
            getattr(witness, 'is_integral_domain', False)
        )
    except Exception:
        h1 = False

    # H2: R^* is the monoid of non-zero elements of R under multiplication
    # This is a definitional hypothesis establishing the notation R^*, 
    # so it holds by definition for the witness.
    h2 = True

    # Conclusion: R is a UFD iff R^* is isomorphic to R^\times \times F
    try:
        # LHS: R is a Unique Factorization Domain
        lhs = bool(getattr(witness, 'is_UFD', False))
        
        # RHS: R^* is isomorphic to R^\times \times F (where F is a free commutative monoid)
        # For commutative domains, this is mathematically equivalent to being a UFD.
        # For non-commutative domains, UFD is False by definition (UFDs are commutative).
        # However, if R is a non-commutative division ring, R^* = R^\times, so 
        # R^* is isomorphic to R^\times \times {0} (where {0} is the free commutative monoid on 0 generators).
        # Thus, for a non-commutative division ring, RHS is True while LHS is False.
        if hasattr(witness, 'is_monoid_isomorphic'):
            rhs = bool(witness.is_monoid_isomorphic)
        else:
            is_comm = getattr(witness, 'is_commutative', True)
            is_div = getattr(witness, 'is_division_ring', False) or getattr(witness, 'is_Field', False)
            
            if is_comm:
                rhs = lhs
            else:
                rhs = is_div
                
        conjecture_holds = (lhs == rhs)
        neg_q = not conjecture_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R^* is the monoid of non-zero elements of R under multiplication",
    "¬Q: The equivalence (R is a UFD iff R^* is isomorphic to R^\\times x F) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2