import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain
from sympy.polys.rings import PolyRing
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "The integral closure of R in its field of fractions is a Krull domain."
    
    Since standard SymPy rings are Noetherian (and thus their integral closures 
    are Krull domains by the Mori-Nagata theorem), a true counterexample must be 
    a non-Noetherian domain (e.g., the ring of all algebraic integers, or a 
    valuation ring of rank > 1). We check for custom objects or strings representing these.
    """
    try:
        # Default to True (meaning it IS a Krull domain, so it's NOT a counterexample)
        is_krull = True
        
        if isinstance(witness, str):
            s = witness.lower()
            # Check for known counterexamples in string format
            if any(kw in s for kw in ["algebraic integer", "valuation", "non-noetherian", "puiseux", "not krull", "not a krull"]):
                is_krull = False
        else:
            # Check for explicit properties on custom witness objects
            if hasattr(witness, 'is_Krull'):
                is_krull = bool(witness.is_Krull)
            elif hasattr(witness, 'is_krull'):
                is_krull = bool(witness.is_krull)
            elif hasattr(witness, 'is_Noetherian'):
                if not witness.is_Noetherian:
                    is_krull = False
            elif hasattr(witness, 'is_noetherian'):
                if not witness.is_noetherian:
                    is_krull = False
            else:
                # Check class name for hints of known counterexamples
                name = witness.__class__.__name__.lower()
                if any(kw in name for kw in ["algebraicinteger", "valuationring", "nonnoetherian"]):
                    is_krull = False
                    
        # neg_Q is True when the conclusion FAILS (i.e., it is NOT a Krull domain)
        neg_q = not is_krull
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The integral closure of R in its field of fractions is not a Krull domain"
]

N_HYP = 0
NEG_Q_INDEX = 0