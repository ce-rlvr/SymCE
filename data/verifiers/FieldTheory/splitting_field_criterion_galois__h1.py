import sympy

class FieldExtension:
    """
    A simple representation of a field extension for testing the conjecture.
    Since SymPy does not natively represent infinite Galois extensions,
    we provide standard examples as named objects.
    """
    def __init__(self, name: str, is_galois: bool, is_finite: bool):
        self.name = name
        self.is_galois = is_galois
        self.is_finite = is_finite
        
    def __repr__(self):
        return f"FieldExtension({self.name})"

# Standard field extensions for the witness namespace
Q_bar_over_Q = FieldExtension("Q_bar/Q", is_galois=True, is_finite=False)
Fp_bar_over_Fp = FieldExtension("Fp_bar/Fp", is_galois=True, is_finite=False)
C_over_R = FieldExtension("C/R", is_galois=True, is_finite=True)
Q_sqrt2_over_Q = FieldExtension("Q(sqrt(2))/Q", is_galois=True, is_finite=True)
Q_cbrt2_over_Q = FieldExtension("Q(cbrt(2))/Q", is_galois=False, is_finite=True)
R_over_Q = FieldExtension("R/Q", is_galois=False, is_finite=False)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_galois') and hasattr(witness, 'is_finite'):
            is_galois = bool(witness.is_galois)
            is_finite = bool(witness.is_finite)
        else:
            return [False]
            
        # A field extension is the splitting field of a single separable polynomial f(x)
        # if and only if it is a FINITE Galois extension.
        is_splitting_field_of_single_poly = is_galois and is_finite
        
        # The false conjecture claims: Galois iff splitting field of a single separable polynomial
        iff_holds = (is_galois == is_splitting_field_of_single_poly)
        
        # The negated conclusion is True when the equivalence fails
        neg_q = not iff_holds
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence (E/F is Galois iff E is the splitting field of a separable polynomial) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0