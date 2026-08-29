import sympy
from sympy import Poly, symbols, QQ, ZZ

# Top-level setup for witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness must be a sympy.Poly object to explicitly define the ring R (its domain).
    """
    # H_1: R is a Unique Factorization Domain
    try:
        if not isinstance(witness, Poly):
            h1 = False
        else:
            h1 = bool(witness.domain.is_UFD)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness
    # Conclusion: f is primitive iff its reduction modulo p is non-zero for all prime elements p in R.
    try:
        if not isinstance(witness, Poly):
            neg_q = False
        else:
            # LHS: f is primitive
            # A polynomial is primitive if the gcd of its coefficients (content) is a unit.
            # The zero polynomial is never primitive.
            if witness.is_zero:
                lhs = False
            else:
                try:
                    lhs = bool(witness.is_primitive)
                except Exception:
                    c = witness.content()
                    lhs = bool(witness.domain.is_unit(c))
            
            # RHS: reduction modulo p is non-zero for all prime elements p in R
            # In a UFD, if R is a field, there are no prime elements, so this condition is vacuously TRUE.
            # If R is not a field, it has prime elements. The reduction modulo p is non-zero for all primes p
            # if and only if no prime divides all coefficients, which means the content is a unit (i.e., f is primitive).
            if witness.domain.is_Field:
                rhs = True
            else:
                rhs = lhs
                
            # The conjecture claims LHS == RHS
            q = (lhs == rhs)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: The equivalence between primitivity and non-zero prime reductions fails"
]

N_HYP = 1
NEG_Q_INDEX = 1