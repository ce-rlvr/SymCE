import sympy

x, y, z = sympy.symbols('x y z')
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (E, F) representing the field extension E/F.
    Example of a valid witness: (QQ.frac_field(x), QQ)
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        E, F = witness
    except Exception:
        return [False, False, False]
        
    # H_1: E is a field
    try:
        h1 = getattr(E, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: F is a subfield of E
    try:
        h2 = False
        if getattr(F, 'is_Field', False) and getattr(E, 'is_Field', False):
            if F == E:
                h2 = True
            elif hasattr(E, 'domain') and F == E.domain:
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The equivalence (E is simple over F iff there are finitely many intermediate fields) fails
    try:
        neg_q = False
        if h1 and h2:
            if E == F:
                is_simple = True
                is_finite_intermediate = True
                neg_q = (is_simple != is_finite_intermediate)
            elif type(E).__name__ == 'FractionField' and F == E.domain:
                # Transcendental extension
                gens = getattr(E, 'gens', getattr(E, 'symbols', []))
                is_simple = (len(gens) == 1)
                is_finite_intermediate = False
                neg_q = (is_simple != is_finite_intermediate)
            elif type(E).__name__ == 'AlgebraicField' and F == E.domain:
                # Finite algebraic extension over QQ
                is_simple = True
                is_finite_intermediate = True
                neg_q = (is_simple != is_finite_intermediate)
            else:
                # Unrecognized extension type; default to False to be safe
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field",
    "H_2: F is a subfield of E",
    "¬Q: The equivalence (E is simple over F iff there are finitely many intermediate fields) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2