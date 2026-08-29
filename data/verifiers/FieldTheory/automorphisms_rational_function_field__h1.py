import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture.
    The true theorem requires K to be a field. The dropped hypothesis is "K is a field".
    Thus, a valid counterexample is an integral domain that is not a field (e.g., ZZ).
    """
    # Translate common sympy Set representations to their Domain equivalents
    try:
        if witness == sympy.S.Integers:
            witness = ZZ
        elif witness == sympy.S.Rationals:
            witness = QQ
        elif witness == sympy.S.Reals:
            witness = RR
        elif witness == sympy.S.Complexes:
            witness = CC
    except Exception:
        pass

    # H_1: K(x) is the field of rational functions in one variable over K
    # This implies K is an integral domain. In sympy, Domains represent integral domains
    # and have the 'get_field' and 'is_Field' attributes.
    try:
        h1 = hasattr(witness, 'get_field') and hasattr(witness, 'is_Field')
    except Exception:
        h1 = False

    # ¬Q: The group of K-automorphisms of K(x) is NOT isomorphic to PGL_2(K)
    # If K is an integral domain but not a field, Aut_K(K(x)) is isomorphic to PGL_2(Frac(K)),
    # which is generally not isomorphic to PGL_2(K) (e.g., PGL_2(QQ) is not isomorphic to PGL_2(ZZ)).
    # Thus, the conclusion fails (¬Q is True) iff K is not a field.
    try:
        if h1:
            neg_q = not witness.is_Field
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K(x) is the field of rational functions in one variable over K",
    "¬Q: The group of K-automorphisms of K(x) is not isomorphic to PGL_2(K)"
]

N_HYP = 1
NEG_Q_INDEX = 1