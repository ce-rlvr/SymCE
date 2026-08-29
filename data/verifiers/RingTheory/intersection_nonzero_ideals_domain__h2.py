import sympy
from sympy import ZZ, QQ, Symbol

# Setup named objects that might be used in the witness
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should represent (R, I_gens, J_gens) or just (I_gens, J_gens) assuming R=ZZ.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I_gens, J_gens = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            R = ZZ
            I_gens, J_gens = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if not isinstance(I_gens, (list, tuple, set)):
            I_gens = [I_gens]
        if not isinstance(J_gens, (list, tuple, set)):
            J_gens = [J_gens]
    except Exception:
        return [False, False, False]

    # H_1: R is an integral domain
    try:
        if R == ZZ or R == QQ:
            h1_ok = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1_ok = True
        elif hasattr(R, 'domain') and R.domain in [ZZ, QQ]:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: J is a non-zero ideal of R
    try:
        # J is non-zero if at least one of its generators is non-zero
        h2_ok = any(g != 0 and (not hasattr(R, 'zero') or g != R.zero) for g in J_gens)
    except Exception:
        h2_ok = False

    # ¬Q: I \cap J is NOT a non-zero ideal of R
    try:
        # In an integral domain, the intersection of two ideals is the zero ideal 
        # if and only if at least one of the ideals is the zero ideal.
        # Since H_2 ensures J is non-zero, I \cap J is zero iff I is the zero ideal.
        # Thus, the conclusion fails (intersection is zero) iff all generators of I are zero.
        neg_q_ok = all(g == 0 or (hasattr(R, 'zero') and g == R.zero) for g in I_gens)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: J is a non-zero ideal of R",
    "¬Q: I \\cap J is not a non-zero ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2