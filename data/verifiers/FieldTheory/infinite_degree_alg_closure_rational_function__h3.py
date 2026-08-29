import sympy
from sympy import QQ, ZZ, RR, CC, GF
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    
    The conjecture states:
    Hypotheses:
      - F is a field
      - F(x) is the field of rational functions in one variable over F
    Conclusion:
      The field extension \overline{F(x)} / F(x) has infinite degree
      
    Mathematically, by the Artin-Schreier theorem, the algebraic closure of a field K 
    has finite degree over K if and only if K is algebraically closed (degree 1) or 
    real closed (degree 2). 
    For K = F(x), the polynomial T^2 - x has no root, so K is never algebraically closed.
    The polynomial T^3 - x has no root, so K is never real closed.
    Thus, the degree of \overline{F(x)} / F(x) is ALWAYS infinite for ANY field F.
    Since the conclusion is always true, its negation is always false.
    """
    # H_1: F is a field
    try:
        if hasattr(witness, 'is_Field'):
            h1_ok = bool(witness.is_Field)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: F(x) is the field of rational functions in one variable over F
    # This is a definitional hypothesis. If F is a field, F(x) is well-defined.
    try:
        h2_ok = h1_ok
    except Exception:
        h2_ok = False

    # ¬Q: The field extension \overline{F(x)} / F(x) has finite degree
    # As proven above, this is mathematically impossible for any valid field F.
    try:
        neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F(x) is the field of rational functions in one variable over F",
    "¬Q: The field extension \\overline{F(x)} / F(x) has finite degree"
]

N_HYP = 2
NEG_Q_INDEX = 2