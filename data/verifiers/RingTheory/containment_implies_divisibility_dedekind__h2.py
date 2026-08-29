import sympy
from sympy import S
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
ZZ = S.Integers
QQ = S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a Dedekind domain R, if I \subseteq J, then there exists an ideal K such that I = JK."
    (The dropped hypothesis is that I and J must be ideals).
    """
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Dedekind domain
    try:
        # We accept standard Dedekind domains like ZZ or QQ
        h1 = (R in ["ZZ", "QQ", ZZ, QQ])
    except Exception:
        h1 = False
        
    # H_2: I \subseteq J
    try:
        if isinstance(I, (set, list, tuple)) and isinstance(J, (set, list, tuple)):
            h2 = set(I).issubset(set(J))
        elif hasattr(I, "is_subset"):
            h2 = bool(I.is_subset(J))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: There does NOT exist an ideal K of R such that I = JK
    # In a Dedekind domain (like ZZ), the product of any subset J and an ideal K is ALWAYS an ideal.
    # Therefore, if I is NOT an ideal, it can never equal JK for any ideal K.
    # Conversely, if I is an ideal and I \subseteq J, such a K always exists.
    # Thus, the conclusion fails (¬Q is True) if and only if I is not an ideal.
    try:
        is_ideal = True
        if isinstance(I, (set, list, tuple)):
            # The only finite ideal in ZZ or QQ is {0}
            is_ideal = (set(I) == {0})
        elif hasattr(I, "is_FiniteSet") and I.is_FiniteSet:
            is_ideal = (list(I) == [0])
        elif hasattr(I, "contains"):
            if not I.contains(0):
                is_ideal = False
            else:
                if hasattr(I, "is_bounded") and I.is_bounded:
                    is_ideal = False
                else:
                    is_ideal = True
        else:
            # Safe fallback: assume it might be an ideal to avoid false positives
            is_ideal = True
            
        neg_q = not is_ideal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "H_2: I is a subset of J",
    "¬Q: There does not exist an ideal K of R such that I = JK"
]

N_HYP = 2
NEG_Q_INDEX = 2