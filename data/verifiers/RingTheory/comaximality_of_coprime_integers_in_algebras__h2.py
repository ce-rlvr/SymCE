import sympy
import math

# Top-level setup for potential witness evaluation
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (m, n), a tuple (R, m, n), or a dictionary with keys 'm', 'n', and optionally 'R'.
    """
    h1 = False
    neg_q = False
    R, m, n = None, 0, 0

    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            R = witness.get('R', ZZ)
            h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer))
            if 'R' in witness:
                h1 = h1 and (R in (ZZ, QQ, 'ZZ', 'QQ', 'Z', 'Q') or hasattr(R, 'is_Ring') or hasattr(R, 'is_ring'))
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                R, m, n = witness
                h1 = R in (ZZ, QQ, 'ZZ', 'QQ', 'Z', 'Q') or hasattr(R, 'is_Ring') or hasattr(R, 'is_ring')
                h1 = h1 and isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer))
            elif len(witness) == 2:
                m, n = witness
                R = ZZ
                h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer))
    except Exception:
        pass

    try:
        if h1:
            m_val = int(m)
            n_val = int(n)
            
            # Check if mR and nR are NOT comaximal in R
            if R in (QQ, 'QQ', 'Q'):
                # In a field like QQ, ideals are comaximal unless both are the zero ideal
                neg_q = (m_val == 0 and n_val == 0)
            else:
                # For ZZ and general rings, if gcd(m, n) != 1, they fail to be comaximal in ZZ
                # and thus provide a valid counterexample for the universal or specific ring R.
                neg_q = (math.gcd(m_val, n_val) != 1)
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Let R be a ring with identity",
    "¬Q: The ideals mR and nR are not comaximal in R"
]

N_HYP = 1
NEG_Q_INDEX = 1