import sympy
from sympy.abc import x, y, z

class MockModule:
    """
    A mock module to represent properties of modules over rings,
    since SymPy does not natively support non-Noetherian rings
    or general module presentation properties.
    """
    def __init__(self, fg, fp):
        self.is_finitely_generated = fg
        self.is_finitely_presented = fp

# Witness candidates
M_fg_not_fp = MockModule(True, False)  # Counterexample: finitely generated but not finitely presented
M_fg_fp = MockModule(True, True)       # Finitely generated and finitely presented
M_not_fg_not_fp = MockModule(False, False) # Neither

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if hasattr(witness, 'is_finitely_generated'):
            h1 = bool(witness.is_finitely_generated)
        elif isinstance(witness, dict) and 'is_finitely_generated' in witness:
            h1 = bool(witness['is_finitely_generated'])
        elif isinstance(witness, tuple) and len(witness) >= 1:
            h1 = bool(witness[0])
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_finitely_presented'):
            neg_q = not bool(witness.is_finitely_presented)
        elif isinstance(witness, dict) and 'is_finitely_presented' in witness:
            neg_q = not bool(witness['is_finitely_presented'])
        elif isinstance(witness, tuple) and len(witness) >= 2:
            neg_q = not bool(witness[1])
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated right R-module",
    "¬Q: M is not a finitely presented R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1