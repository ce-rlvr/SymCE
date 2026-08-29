import sympy

# Top-level setup: named object bindings
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
ZZ = sympy.ZZ
Q = sympy.QQ
R = sympy.RR
C = sympy.CC
Z = sympy.ZZ

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    
    Conjecture:
      H1: Let F be a field
      H2: Let F be an ordered field
      Conclusion: The field \overline{F} cannot be equipped with a strict total order that makes it an ordered field.
      
    Note: The conclusion is mathematically unconditionally true for all fields, because the algebraic 
    closure \overline{F} is algebraically closed and thus contains a square root of -1. In any ordered 
    field, squares must be non-negative, so -1 >= 0, which implies 1 <= 0, a contradiction. 
    Therefore, \overline{F} can NEVER be an ordered field. The negated conclusion is always False.
    """
    # H_1: Let F be a field
    try:
        h1 = False
        if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, sympy.QQ, sympy.RR, sympy.CC):
            h1 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        elif hasattr(witness, 'is_field') and witness.is_field:
            h1 = True
        elif type(witness).__name__ in ('RationalField', 'RealField', 'ComplexField', 'GaloisField', 'AlgebraicField', 'FractionField'):
            h1 = True
    except Exception:
        h1 = False

    # H_2: Let F be an ordered field
    try:
        h2 = False
        if h1:
            if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.QQ, sympy.RR):
                h2 = True
            elif witness in (sympy.S.Complexes, sympy.CC):
                h2 = False
            else:
                char = None
                if hasattr(witness, 'characteristic') and callable(witness.characteristic):
                    char = witness.characteristic()
                elif hasattr(witness, 'char'):
                    char = witness.char
                
                if char is not None and char != 0:
                    h2 = False
                else:
                    if type(witness).__name__ == 'ComplexField':
                        h2 = False
                    else:
                        try:
                            # If it contains the imaginary unit, it cannot be ordered
                            if sympy.I in witness:
                                h2 = False
                            else:
                                h2 = True
                        except Exception:
                            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The field \overline{F} CAN be equipped with a strict total order that makes it an ordered field.
    # As proven above, this is mathematically impossible.
    neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F is an ordered field",
    "¬Q: The field \\overline{F} can be equipped with a strict total order that makes it an ordered field"
]

N_HYP = 2
NEG_Q_INDEX = 2