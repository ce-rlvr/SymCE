import sympy
from sympy import QQ, ZZ

# Top-level setup
# QQ and ZZ are available for witness construction.

def conditions(witness):
    R = None
    I_gens = []
    
    try:
        # Parse the witness. It can be a tuple (Ring, Ideal_Generators),
        # a SymPy Ideal object, or just a Field (implying I = R).
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I_gens = witness
        elif hasattr(witness, 'ring') and hasattr(witness, 'gens'):
            R = witness.ring
            I_gens = witness.gens
        elif getattr(witness, 'is_Field', False) or witness.__class__.__name__ == 'FiniteField':
            R = witness
            I_gens = [getattr(R, 'one', 1)]
            
        if not isinstance(I_gens, (list, tuple, set)):
            I_gens = [I_gens]
    except Exception:
        pass

    # H_1: R is a Noetherian local ring
    try:
        h1 = False
        if R is not None:
            # In SymPy, fields are the most accessible Noetherian local rings.
            if getattr(R, 'is_Field', False) or R.__class__.__name__ == 'FiniteField':
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: \bigcap_{n=1}^{\infty} I^n \neq \{0\}
    try:
        neg_q = False
        if R is not None:
            # In a Noetherian local ring, \bigcap I^n = {0} iff I is a proper ideal.
            # Thus, the intersection is NOT {0} iff I is not proper (i.e., I == R).
            if getattr(R, 'is_Field', False) or R.__class__.__name__ == 'FiniteField':
                # For a field, I == R iff the ideal contains any non-zero element.
                zero = getattr(R, 'zero', 0)
                if any(g != zero for g in I_gens):
                    neg_q = True
            else:
                # Fallback for other rings: check if 1 is explicitly in the generators.
                if hasattr(R, 'one') and R.one in I_gens:
                    neg_q = True
                elif 1 in I_gens:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian local ring",
    "¬Q: \\bigcap_{n=1}^{\\infty} I^n \\neq \\{0\\}"
]

N_HYP = 1
NEG_Q_INDEX = 1