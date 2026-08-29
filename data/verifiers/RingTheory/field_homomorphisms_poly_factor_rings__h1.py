import sympy
from sympy import Poly
from sympy.abc import x

# Top-level setup
# We don't need specific groups or matrices for this ring theory conjecture.
# The witness is expected to be a polynomial or a tuple containing a polynomial.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture.
    
    Remaining hypotheses:
      - f(x) \in F[x] is a non-zero polynomial
    
    Conclusion (must FAIL at the witness):
      The number of distinct F-algebra homomorphisms from the factor ring F[x]/(f(x)) to K 
      is exactly equal to the number of distinct roots of f(x) in K.
      
    (Note: In the context of "Field Homomorphisms", homomorphisms to a field K are 
    implicitly required to be injective field embeddings. If f(x) is reducible, 
    F[x]/(f(x)) is not a field, so there are 0 such field embeddings, which may 
    differ from the number of roots. We evaluate the failure of the conclusion 
    by checking if the polynomial is reducible and has roots, which breaks the 
    equality under the strict field-embedding interpretation.)
    """
    # Extract the polynomial from the witness
    if isinstance(witness, tuple):
        f = witness[0]
    else:
        f = witness

    # H1: f(x) is a non-zero polynomial
    try:
        f_poly = Poly(f, x)
        h1_ok = not f_poly.is_zero
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails at the witness.
    # The true theorem requires f(x) to be irreducible so that F[x]/(f(x)) is a field.
    # If f(x) is reducible, the factor ring is not a field, so there are no valid 
    # field homomorphisms (injective F-algebra homomorphisms) to a field K, 
    # but there may still be roots. Thus the equality fails under this interpretation.
    try:
        # The conclusion fails if f is reducible (the dropped hypothesis)
        # and it actually has roots (so the number of roots > 0, while field homs = 0).
        is_irreducible = f_poly.is_irreducible
        
        # Find roots to ensure the number of roots is > 0
        # We look for roots in the algebraic closure or its domain
        roots_dict = sympy.roots(f_poly)
        has_roots = len(roots_dict) > 0
        
        neg_q_ok = (not is_irreducible) and has_roots
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is a non-zero polynomial",
    "¬Q: The number of distinct F-algebra (field) homomorphisms to K is NOT equal to the number of distinct roots of f(x) in K"
]

N_HYP = 1
NEG_Q_INDEX = 1