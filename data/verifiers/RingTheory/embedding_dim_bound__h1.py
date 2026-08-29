import math
import sympy
from sympy import Rational, Integer, Symbol

class LocalRing:
    """
    A mock object representing a local ring for the purpose of verifying
    the Embedding Dimension Bound conjecture.
    """
    def __init__(self, krull_dimension, m_mod_m2_dimension, has_residue_field=True):
        self.krull_dimension = krull_dimension
        self.m_mod_m2_dimension = m_mod_m2_dimension
        self.has_residue_field = has_residue_field

def conditions(witness) -> list[bool]:
    # H_1: k = R/m is the residue field of R.
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('has_residue_field', False))
        else:
            h1 = bool(getattr(witness, 'has_residue_field', False))
    except Exception:
        h1 = False

    # ¬Q: The vector space dimension of m/m^2 over k is NOT (finite AND >= Krull dimension)
    try:
        if isinstance(witness, dict):
            m_dim = witness.get('m_mod_m2_dimension', 0)
            k_dim = witness.get('krull_dimension', 0)
        else:
            m_dim = getattr(witness, 'm_mod_m2_dimension', 0)
            k_dim = getattr(witness, 'krull_dimension', 0)
        
        is_finite = (m_dim != math.inf) and (m_dim != float('inf')) and (m_dim != sympy.oo)
        q = is_finite and bool(m_dim >= k_dim)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k = R/m is the residue field of R",
    "¬Q: The vector space dimension of m/m^2 over k is infinite or less than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1