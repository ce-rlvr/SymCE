import sympy

class FieldObj:
    def __init__(self, name):
        self.name = name
        self.is_field = True

class ExtensionObj:
    def __init__(self, base, is_finite, is_normal, is_splitting_field_of_single_poly):
        self.base_field = base
        self.is_finite = is_finite
        self.is_normal = is_normal
        self.is_splitting_field_of_single_poly = is_splitting_field_of_single_poly

# Standard counterexample: The algebraic closure of Q is an infinite normal extension,
# but it is not the splitting field of any single polynomial in Q[x].
Q = FieldObj("Q")
Q_alg = ExtensionObj(Q, is_finite=False, is_normal=True, is_splitting_field_of_single_poly=False)

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2:
            F, K = witness
        else:
            K = witness
            F = getattr(K, 'base_field', None)
            if F is None:
                if isinstance(K, str):
                    F = "Q"
                else:
                    return [False, False]

        # H_1: F is a field
        h1 = False
        if getattr(F, 'is_field', False) or getattr(F, 'is_Field', False):
            h1 = True
        elif isinstance(F, str) and F.lower() in ['q', 'r', 'c', 'fp', 'qq', 'f']:
            h1 = True

        # ¬Q: K is a normal extension iff K is the splitting field of some polynomial f(x) in F[x]
        # The conclusion fails if the equivalence does not hold.
        neg_q = False
        if hasattr(K, 'is_normal') and hasattr(K, 'is_splitting_field_of_single_poly'):
            neg_q = bool(K.is_normal != K.is_splitting_field_of_single_poly)
        elif isinstance(K, str):
            k_str = K.lower()
            # Infinite normal extensions are the standard counterexamples
            if 'alg' in k_str or 'closure' in k_str or 'infinite' in k_str:
                neg_q = True

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: K is a normal extension of F but not the splitting field of a single polynomial over F (or vice versa)"
]

N_HYP = 1
NEG_Q_INDEX = 1