import sympy
from sympy.polys.domains import FF, QQ, RR, CC, ZZ
from sympy.ntheory import factorint

# Top-level setup
F2 = FF(2)
F3 = FF(3)
F4 = 4  # Represented by its order
F5 = FF(5)
F7 = FF(7)
F8 = 8  # Represented by its order
F9 = 9  # Represented by its order

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # A finite field can be represented by its order (a prime power)
        if isinstance(witness, int) and not isinstance(witness, bool):
            if witness >= 2 and len(factorint(witness)) == 1:
                h1 = True
                # The algebraic closure of a finite field is countably infinite,
                # so its cardinality is not equal to the finite field's cardinality.
                neg_q = True
        else:
            # Alternatively, the witness can be a SymPy domain object
            if hasattr(witness, 'is_Field') and witness.is_Field:
                h1 = True
                name = type(witness).__name__
                if name in ['FiniteField', 'GaloisField', 'FF']:
                    neg_q = True
                elif witness in [QQ, RR, CC]:
                    neg_q = False
                else:
                    # Fallback for other domain objects
                    if hasattr(witness, 'order') and witness.order != float('inf'):
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The cardinality of the algebraic closure of F is not equal to the cardinality of F"
]

N_HYP = 1
NEG_Q_INDEX = 1