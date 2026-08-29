import sympy
from sympy import ZZ, QQ, Symbol, I

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and the negated conclusion.
    
    Conjecture: R is not a Euclidean domain.
    Remaining hypotheses: (none)
    Negated conclusion (¬Q): R IS a Euclidean domain.
    """
    try:
        neg_q = False
        
        # Check if the witness is a Euclidean domain
        if getattr(witness, 'is_Field', False):
            neg_q = True
        elif witness == ZZ:
            neg_q = True
        elif witness == sympy.S.Integers:
            neg_q = True
        elif witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            neg_q = True
        elif witness.__class__.__name__ == 'GaussianIntegerRing':
            neg_q = True
        elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            # F[x] is a Euclidean domain if F is a field and there is only 1 variable
            if getattr(witness.domain, 'is_Field', False) and len(witness.symbols) == 1:
                neg_q = True
        elif getattr(witness, 'is_PID', False):
            # In SymPy's domain system, implemented PIDs are typically Euclidean domains
            neg_q = True
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is a Euclidean domain"
]

N_HYP = 0
NEG_Q_INDEX = 0