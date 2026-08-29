import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
# QQ_xy represents the polynomial ring Q[x, y], where (x) is prime but not maximal.
QQ_xy = QQ[x, y]
ZZ_x = ZZ[x]

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be an ideal (e.g., QQ_xy.ideal(x)) or a tuple (Ring, generators).
    """
    # If witness is provided as (Ring, generators), attempt to construct the ideal
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, gens = witness
            if hasattr(ring, 'ideal'):
                if isinstance(gens, (list, tuple)):
                    witness = ring.ideal(*gens)
                else:
                    witness = ring.ideal(gens)
    except Exception:
        pass

    # H_1: P is a non-zero prime ideal of R
    try:
        is_nonzero = False
        if hasattr(witness, 'is_zero'):
            z_val = witness.is_zero() if callable(witness.is_zero) else witness.is_zero
            is_nonzero = not bool(z_val)
        elif hasattr(witness, 'gens'):
            is_nonzero = not all(g == 0 for g in witness.gens)
        else:
            # Fallback if we cannot explicitly check for zero
            is_nonzero = True
            
        is_prime = False
        if hasattr(witness, 'is_prime'):
            p_val = witness.is_prime() if callable(witness.is_prime) else witness.is_prime
            is_prime = bool(p_val)
            
        h1_ok = is_nonzero and is_prime
    except Exception:
        h1_ok = False

    # ¬Q: P is NOT a maximal ideal in R
    try:
        is_maximal = True
        if hasattr(witness, 'is_maximal'):
            m_val = witness.is_maximal() if callable(witness.is_maximal) else witness.is_maximal
            is_maximal = bool(m_val)
            
        neg_q_ok = not is_maximal
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a non-zero prime ideal of R",
    "¬Q: P is not a maximal ideal in R"
]

N_HYP = 1
NEG_Q_INDEX = 1