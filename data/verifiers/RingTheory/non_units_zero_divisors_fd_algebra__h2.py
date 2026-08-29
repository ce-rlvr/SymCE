import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z, t

# Top-level setup
# The witness is expected to provide the field k, the algebra A, and the element x.
# For example, a valid counterexample witness could be:
# witness = (QQ, QQ['t'], QQ['t'].gens[0])

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (k, A, x) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            k = witness.get('k')
            A = witness.get('A')
            x_elem = witness.get('x')
        else:
            k, A, x_elem = witness
    except Exception:
        return [False, False, False]

    # H_1: Let k be a field
    try:
        h1 = bool(getattr(k, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: Let x \in A be an element that is not a unit
    try:
        in_A = (x_elem in A)
        
        if hasattr(A, 'is_unit'):
            is_unit = bool(A.is_unit(x_elem))
        else:
            try:
                # In sympy domains, exact division of 1 by x succeeds iff x is a unit
                A.exquo(A.one, x_elem)
                is_unit = True
            except Exception:
                is_unit = False
                
        h2 = in_A and not is_unit
    except Exception:
        h2 = False

    # neg_Q: The element x is NEITHER a left zero divisor NOR a right zero divisor in A
    try:
        if hasattr(A, 'is_zero_divisor'):
            is_zd = bool(A.is_zero_divisor(x_elem))
        elif hasattr(A, 'exquo') and hasattr(A, 'zero'):
            # For sympy integral domains (which implement exquo and zero), 
            # the only zero divisor is 0.
            is_zd = (x_elem == A.zero)
        else:
            # If we cannot determine if it's a zero divisor, assume it is 
            # to safely fail the counterexample check.
            is_zd = True
            
        neg_q = not is_zd
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: x in A is an element that is not a unit",
    "¬Q: x is neither a left nor a right zero divisor in A"
]

N_HYP = 2
NEG_Q_INDEX = 2