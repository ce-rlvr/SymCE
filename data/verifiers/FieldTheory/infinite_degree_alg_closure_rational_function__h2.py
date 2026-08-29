import sympy
from sympy import Symbol

# No specific named bindings required for this FieldTheory conjecture.
# Witnesses are typically SymPy domains like sympy.CC or tuples like (sympy.CC, 1).

def conditions(witness):
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    The dropped hypothesis is that x is transcendental over F.
    If x is algebraic over F (e.g., x=1), F(x) is a finite extension of F.
    Then the algebraic closure of F(x) has finite degree iff F is real closed or algebraically closed.
    """
    if isinstance(witness, tuple):
        if len(witness) >= 2:
            F = witness[0]
            x = witness[1]
        else:
            F = witness[0]
            x = 1
    else:
        F = witness
        x = 1

    # H_1: F is a field
    try:
        h1 = False
        if F in [sympy.QQ, sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
        elif type(F).__name__ in ['GaloisField', 'AlgebraicField', 'RealField', 'ComplexField']:
            h1 = True
    except Exception:
        h1 = False

    # H_2: \overline{F(x)} is an algebraic closure of F(x)
    # This is a definitional property of the algebraic closure object.
    # We assume the witness implicitly provides the standard algebraic closure.
    h2 = True

    # neg_Q: The field extension \overline{F(x)} / F(x) has finite degree
    try:
        neg_q = False
        # If x has free symbols, it's transcendental, so F(x) is the rational function field.
        # The algebraic closure of a rational function field ALWAYS has infinite degree.
        if hasattr(x, 'free_symbols') and x.free_symbols:
            neg_q = False
        else:
            # If x is a constant/algebraic, F(x) is a finite extension of F.
            # The algebraic closure has finite degree iff F is real closed or algebraically closed.
            if F in [sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes]:
                neg_q = True
            elif hasattr(F, 'is_RealField') and F.is_RealField:
                neg_q = True
            elif hasattr(F, 'is_ComplexField') and F.is_ComplexField:
                neg_q = True
            elif hasattr(F, 'is_algebraically_closed') and F.is_algebraically_closed:
                neg_q = True
            elif hasattr(F, 'is_real_closed') and F.is_real_closed:
                neg_q = True
            elif str(F) in ['RR', 'CC', 'Reals', 'Complexes', 'AlgebraicNumbers']:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: \\overline{F(x)} is an algebraic closure of F(x)",
    "¬Q: The field extension \\overline{F(x)} / F(x) has finite degree"
]

N_HYP = 2
NEG_Q_INDEX = 2