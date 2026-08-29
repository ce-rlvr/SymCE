import sympy
from sympy.polys.domains import Domain, ExpressionDomain
from sympy.abc import x, y, z

# Top-level setup
EX = sympy.EX
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    The conjecture is "R is a Noetherian ring" (with no remaining hypotheses).
    We need to verify that the witness is NOT a Noetherian ring.
    """
    try:
        is_noeth = True
        
        if hasattr(witness, 'is_Noetherian'):
            is_noeth = bool(witness.is_Noetherian)
        elif hasattr(witness, 'is_noetherian'):
            is_noeth = bool(witness.is_noetherian)
        elif isinstance(witness, ExpressionDomain):
            # The expression domain in SymPy is not Noetherian
            is_noeth = False
        elif isinstance(witness, Domain):
            # Standard SymPy domains (ZZ, QQ, finite extensions, poly rings in finite vars) are Noetherian
            is_noeth = True
        elif isinstance(witness, str):
            s = witness.lower()
            if "not noetherian" in s or "non-noetherian" in s:
                is_noeth = False
            elif "infinite" in s and ("variables" in s or "generators" in s or "indeterminates" in s):
                is_noeth = False
            elif "..." in s:
                is_noeth = False
            elif "continuous functions" in s:
                is_noeth = False
        else:
            # Default to True so that unrecognized objects fail the counterexample check
            is_noeth = True
            
        neg_q = not is_noeth
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 0
NEG_Q_INDEX = 0