import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for Ring Theory
# (Using standard symbols and base rings as relevant for commutative algebras)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    Witness can be a dictionary/object with boolean properties, or a tuple (k, R, I) / (R, I).
    """
    # Dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_commutative_k_algebra', False))
            h2 = bool(witness.get('is_fg_k_algebra', False))
            h3 = bool(witness.get('is_ideal', False))
            neg_q = not bool(witness.get('quotient_is_fg_k_algebra', True))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass
            
    # Object witness
    if hasattr(witness, 'is_commutative_k_algebra'):
        try:
            h1 = bool(getattr(witness, 'is_commutative_k_algebra', False))
            h2 = bool(getattr(witness, 'is_fg_k_algebra', False))
            h3 = bool(getattr(witness, 'is_ideal', False))
            neg_q = not bool(getattr(witness, 'quotient_is_fg_k_algebra', True))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass
            
    # Tuple witness (k, R, I) or (R, I)
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                k, R, I = witness
            elif len(witness) == 2:
                R, I = witness
            else:
                return [False, False, False, False]
            
            # H1: R is a commutative k-algebra
            h1 = bool(getattr(R, 'is_commutative', False))
            
            # H2: R is finitely generated as a k-algebra
            # In sympy, PolyRing and QuotientRing over a field/ring are finitely generated
            h2 = type(R).__name__ in ('PolyRing', 'QuotientRing')
            
            # H3: I is an ideal of R
            if isinstance(I, (list, tuple)):
                h3 = all(e in R for e in I)
            elif type(I).__name__ == 'Ideal':
                h3 = getattr(I, 'ring', None) == R
            else:
                h3 = False
                
            # ¬Q: R/I is not finitely generated as a k-algebra
            # Mathematically, if R is a finitely generated k-algebra, any quotient R/I 
            # is ALWAYS a finitely generated k-algebra. Thus, the conclusion is always true,
            # and its negation is always false for valid sympy ring objects.
            neg_q = False
            
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative k-algebra",
    "H_2: R is finitely generated as a k-algebra",
    "H_3: I is an ideal of R",
    "¬Q: The quotient ring R/I is not finitely generated as a k-algebra"
]

N_HYP = 3
NEG_Q_INDEX = 3