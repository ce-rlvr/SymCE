import sympy
from sympy import ZZ, QQ

# Top-level setup for standard rings
Z = ZZ
Q = QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let f: R -> S be a ring epimorphism. Then f is surjective."
    
    The witness should be a tuple (R, S, f) where R and S are rings (e.g., ZZ and QQ)
    and f is a callable representing the homomorphism.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, f = witness
        else:
            R = witness.R
            S = witness.S
            f = witness.f
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        # Check if f is a ring homomorphism on a test set of integers
        is_hom = True
        test_elements = [-2, -1, 0, 1, 2]
        for a in test_elements:
            for b in test_elements:
                if f(a + b) != f(a) + f(b):
                    is_hom = False
                if f(a * b) != f(a) * f(b):
                    is_hom = False
        if f(1) != 1:
            is_hom = False

        if is_hom:
            # Check if f is an epimorphism.
            # The standard counterexample is the inclusion of a domain into its fraction field.
            if R == ZZ and S == QQ:
                h1_ok = True
            elif hasattr(R, 'get_field') and S == R.get_field():
                h1_ok = True
            elif hasattr(R, 'frac_field') and S == R.frac_field():
                h1_ok = True
            elif R == S:
                # Identity map is an epimorphism (though not a counterexample to surjectivity)
                is_id = True
                for a in test_elements:
                    if f(a) != a:
                        is_id = False
                if is_id:
                    h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        # Check if f is NOT surjective.
        # The inclusion of a non-field domain into its fraction field is not surjective.
        if R == ZZ and S == QQ:
            neg_q_ok = True
        elif hasattr(R, 'get_field') and S == R.get_field():
            if hasattr(R, 'is_Field') and not R.is_Field:
                neg_q_ok = True
        elif hasattr(R, 'frac_field') and S == R.frac_field():
            if hasattr(R, 'is_Field') and not R.is_Field:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a ring epimorphism",
    "¬Q: f is not surjective"
]

N_HYP = 1
NEG_Q_INDEX = 1