import sympy
from sympy import QQ, ZZ, symbols
from sympy.abc import x, y, z

# Top-level setup
# The witness is expected to be a sympy ring/domain (e.g., ZZ, QQ, QQ[x]).

def conditions(witness):
    """
    Check the hypotheses and negated conclusion for the given witness.
    """
    try:
        # Extract the ring R if the witness is passed as a tuple
        if isinstance(witness, tuple):
            R = witness[0]
        else:
            R = witness
            
        # H_1: Let R be an integral domain
        h1 = bool(R.is_domain)
    except Exception:
        h1 = False

    # H_2: Let K be the field of fractions of R
    # H_3: Let S be the integral closure of R in \overline{K}
    # These are definitions that are mathematically well-defined for any integral domain.
    h2 = h1
    h3 = h1

    # ¬Q: The field of fractions of S is not exactly \overline{K}
    # Mathematically, for ANY integral domain R, the field of fractions of its 
    # integral closure in the algebraic closure of its field of fractions is 
    # ALWAYS exactly the algebraic closure.
    # (Proof: Let x in \overline{K}. x is algebraic over K, so it satisfies a 
    # polynomial with coefficients in K. By clearing denominators (multiplying 
    # by the product of denominators d in R), dx is integral over R, so dx in S.
    # Then x = dx / d is in the field of fractions of S. Thus, the field of 
    # fractions of S contains \overline{K}, and hence equals \overline{K}.)
    # Since the conclusion is a mathematical tautology for all integral domains, 
    # it never fails. Therefore, its negation is always False.
    neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: S is the integral closure of R in the algebraic closure of K",
    "¬Q: The field of fractions of S is not exactly the algebraic closure of K"
]

N_HYP = 3
NEG_Q_INDEX = 3