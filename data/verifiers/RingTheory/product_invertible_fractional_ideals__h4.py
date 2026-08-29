import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the false conjecture:
    "If R is an integral domain, K is its field of fractions, and I is a non-zero 
    invertible fractional ideal of R, then for any fractional ideal J, the product 
    ideal IJ is an invertible fractional ideal, and its inverse is the product of 
    the inverses of I and J."
    
    The dropped hypothesis was that J must also be a non-zero invertible fractional ideal.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            I = witness.get('I')
            J = witness.get('J')
        else:
            R, K, I, J = witness
    except Exception:
        return [False, False, False, False]

    # Helper to extract a single generator if the ideal is provided as a list/tuple/set
    def get_gen(ideal):
        if isinstance(ideal, (list, tuple, set)):
            lst = list(ideal)
            if len(lst) == 1:
                return lst[0]
            elif len(lst) == 0:
                return 0
            else:
                raise ValueError("Multiple generators not supported in this simple check")
        return ideal

    try:
        I_gen = sympy.sympify(get_gen(I))
    except Exception:
        I_gen = get_gen(I)

    try:
        J_gen = sympy.sympify(get_gen(J))
    except Exception:
        J_gen = get_gen(J)

    # H_1: R is an integral domain
    try:
        h1 = False
        if R == ZZ or R == QQ:
            h1 = True
        elif hasattr(R, 'get_field'):
            h1 = True
        elif hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain:
            h1 = True
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        h2 = False
        if R == ZZ and K == QQ:
            h2 = True
        elif hasattr(R, 'get_field') and K == R.get_field():
            h2 = True
    except Exception:
        h2 = False

    # H_3: I is a non-zero invertible fractional ideal of R
    try:
        h3 = False
        if I_gen != 0:
            # Check if it's invertible (for principal ideals represented by their generator)
            inv_I = 1 / I_gen
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The product ideal IJ is not an invertible fractional ideal, 
    # or its inverse is not the product of the inverses of I and J.
    try:
        neg_q = False
        IJ_gen = I_gen * J_gen
        if IJ_gen == 0:
            # The zero ideal is not invertible
            neg_q = True
        else:
            inv_I = 1 / I_gen
            inv_J = 1 / J_gen
            inv_IJ = 1 / IJ_gen
            if sympy.simplify(inv_IJ - (inv_I * inv_J)) != 0:
                neg_q = True
    except Exception:
        # If any operation fails (e.g., 1/J when J=0), the conclusion fails.
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: I is a non-zero invertible fractional ideal of R",
    "¬Q: The product ideal IJ is not an invertible fractional ideal, or its inverse is not the product of the inverses of I and J"
]

N_HYP = 3
NEG_Q_INDEX = 3