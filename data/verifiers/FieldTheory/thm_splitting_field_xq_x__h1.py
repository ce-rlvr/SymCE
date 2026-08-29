import sympy
from sympy import isprime

# Top-level setup
# (No specific named objects needed for this FieldTheory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # If the witness is explicitly a finite field, the original theorem holds.
        if hasattr(witness, 'is_Field') and witness.is_Field:
            q = int(witness.order)
            return [q >= 2, False]
        if type(witness).__name__ == 'GaloisField':
            q = int(witness.order)
            return [q >= 2, False]
            
        # Otherwise, we interpret the witness as the integer q, representing the ring Z/qZ.
        if isinstance(witness, int):
            q = witness
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            q = int(witness)
        elif isinstance(witness, tuple):
            q = int(witness[0])
        else:
            q = int(witness)
            
        # H_1: The order of F is q
        # We require the ring to have at least 2 elements.
        h1 = (q >= 2)
        
        # ¬Q: The polynomial x^q - x does not factor completely over F, 
        # or its roots are not precisely the elements of F.
        # In the ring Z/qZ, this conclusion fails if and only if q is composite.
        # (If q is prime, Z/qZ is a field and the conclusion holds).
        neg_q = not isprime(q)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: The order of F is q",
    "¬Q: The polynomial x^q - x does not factor completely over F or its roots are not precisely the elements of F"
]

N_HYP = 1
NEG_Q_INDEX = 1