import sympy
import math

# Top-level setup
# SymPy does not natively support non-Noetherian rings or homological algebra 
# functors like Tor and Ext. Therefore, the witness is expected to be a dictionary 
# or an object containing the truth values of the hypotheses and the conclusion 
# for a known mathematical counterexample (e.g., over a non-Noetherian ring R).

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Expects a dictionary or object with the following keys/attributes:
      - M_is_finitely_generated: bool
      - N_is_finitely_generated: bool
      - i: int
      - Tor_and_Ext_are_finitely_generated: bool
    """
    # H_1: M is a finitely generated R-module
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('M_is_finitely_generated', False))
        else:
            h1 = bool(getattr(witness, 'M_is_finitely_generated', False))
    except Exception:
        h1 = False

    # H_2: N is a finitely generated R-module
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('N_is_finitely_generated', False))
        else:
            h2 = bool(getattr(witness, 'N_is_finitely_generated', False))
    except Exception:
        h2 = False

    # H_3: i is a non-negative integer
    try:
        if isinstance(witness, dict):
            i_val = witness.get('i', -1)
        else:
            i_val = getattr(witness, 'i', -1)
        h3 = isinstance(i_val, int) and i_val >= 0
    except Exception:
        h3 = False

    # ¬Q: Tor_i^R(M, N) and Ext^i_R(M, N) are NOT finitely generated R-modules
    try:
        if isinstance(witness, dict):
            if 'Tor_and_Ext_are_finitely_generated' in witness:
                neg_q = not bool(witness['Tor_and_Ext_are_finitely_generated'])
            else:
                neg_q = False
        else:
            if hasattr(witness, 'Tor_and_Ext_are_finitely_generated'):
                neg_q = not bool(getattr(witness, 'Tor_and_Ext_are_finitely_generated'))
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "H_2: N is a finitely generated R-module",
    "H_3: i is a non-negative integer",
    "¬Q: Tor_i^R(M, N) and Ext^i_R(M, N) are not both finitely generated R-modules"
]

N_HYP = 3
NEG_Q_INDEX = 3