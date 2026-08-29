import sympy
import sympy.polys
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

# Provide FF for finite fields (e.g., FF(5))
FF = sympy.polys.domains.FF

def conditions(witness):
    try:
        # H_1: R is a Euclidean domain
        # In SymPy, fields, ZZ, and univariate polynomial rings over fields are Euclidean domains.
        h1_ok = False
        if getattr(witness, 'is_Field', False):
            h1_ok = True
        elif witness == ZZ:
            h1_ok = True
        elif hasattr(witness, 'domain') and hasattr(witness, 'gens'):
            if getattr(witness.domain, 'is_Field', False) and len(witness.gens) == 1:
                h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # ¬Q: The intersection of all non-zero ideals of R is not the zero ideal.
        # If R is a field, its only non-zero ideal is R itself. 
        # The intersection of all non-zero ideals is therefore R.
        # Since R is a field (1 != 0), R is not the zero ideal, so the conclusion fails.
        # If R is a Euclidean domain but not a field, the intersection of all non-zero ideals is {0}.
        neg_q_ok = False
        if getattr(witness, 'is_Field', False):
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: The intersection of all non-zero ideals of R is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1