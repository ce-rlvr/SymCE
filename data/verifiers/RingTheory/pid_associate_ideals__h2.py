import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: It is not the case that a and b are associates if and only if (a) = (b)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # Try to extract R, a, b from the witness
    R = None
    a = None
    b = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
        else:
            R = witness.R
            a = witness.a
            b = witness.b
    except Exception:
        # The witness might directly provide the evaluated booleans
        try:
            h1 = bool(witness.is_PID)
            are_assoc = bool(witness.are_associates)
            same_id = bool(witness.same_ideal)
            return [h1, are_assoc != same_id]
        except Exception:
            pass

    if R is None:
        return [False, False]

    # Check H1: R is a principal ideal domain
    try:
        if hasattr(R, 'is_PID'):
            h1 = bool(R.is_PID() if callable(R.is_PID) else R.is_PID)
        elif hasattr(R, 'is_principal_ideal_domain'):
            h1 = bool(R.is_principal_ideal_domain() if callable(R.is_principal_ideal_domain) else R.is_principal_ideal_domain)
        else:
            h1 = False
    except Exception:
        h1 = False

    # Check if a and b are associates
    try:
        if hasattr(R, 'are_associates'):
            are_assoc = bool(R.are_associates(a, b))
        elif hasattr(R, 'is_associate'):
            are_assoc = bool(R.is_associate(a, b))
        elif hasattr(R, 'units'):
            units = R.units() if callable(R.units) else R.units
            if hasattr(R, 'mul'):
                are_assoc = any(a == R.mul(u, b) for u in units)
            else:
                are_assoc = any(a == u * b for u in units)
        elif hasattr(R, 'rem'):
            # Fallback for SymPy domains
            a_div_b = (R.rem(a, b) == 0) if b != 0 else (a == 0)
            b_div_a = (R.rem(b, a) == 0) if a != 0 else (b == 0)
            are_assoc = a_div_b and b_div_a
        else:
            are_assoc = False
    except Exception:
        are_assoc = False

    # Check if (a) == (b)
    try:
        if hasattr(R, 'same_ideal'):
            same_id = bool(R.same_ideal(a, b))
        elif hasattr(R, 'ideal'):
            same_id = (R.ideal(a) == R.ideal(b))
        elif hasattr(R, 'rem'):
            # Fallback for SymPy domains
            a_div_b = (R.rem(a, b) == 0) if b != 0 else (a == 0)
            b_div_a = (R.rem(b, a) == 0) if a != 0 else (b == 0)
            same_id = a_div_b and b_div_a
        elif hasattr(R, 'divides'):
            same_id = bool(R.divides(a, b) and R.divides(b, a))
        else:
            same_id = False
    except Exception:
        same_id = False

    # Evaluate negated conclusion
    try:
        conclusion = (are_assoc == same_id)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]