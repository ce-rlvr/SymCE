import sympy

class CustomField:
    def __init__(self, name, field, alg_closed, sep_closed):
        self.name = name
        self.is_Field = field
        self.is_alg_closed = alg_closed
        self.is_sep_closed = sep_closed
        
    def __str__(self):
        return self.name

# Top-level setup: named object bindings that the witness expression may reference.
QQ = CustomField("QQ", True, False, False)
CC = CustomField("CC", True, True, True)
RR = CustomField("RR", True, False, False)
# F_p(t)^{sep} is separably closed but not algebraically closed (lacks p-th roots of t)
Fp_t_sep = CustomField("Fp_t_sep", True, False, True)
Fp_t_alg = CustomField("Fp_t_alg", True, True, True)

def conditions(witness) -> list[bool]:
    if isinstance(witness, str):
        witness = globals().get(witness, witness)
        
    try:
        if hasattr(witness, 'is_Field'):
            h1 = bool(witness.is_Field)
        elif hasattr(witness, 'is_field'):
            h1 = bool(witness.is_field)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_alg_closed'):
            alg_closed = bool(witness.is_alg_closed)
        elif witness == sympy.CC:
            alg_closed = True
        else:
            alg_closed = False
            
        if hasattr(witness, 'is_sep_closed'):
            sep_closed = bool(witness.is_sep_closed)
        elif witness == sympy.CC:
            sep_closed = True
        else:
            sep_closed = False
            
        # The absolute Galois group Gal(K^{sep}/K) is trivial iff K is separably closed.
        # The conclusion states: K is algebraically closed iff Gal(K^{sep}/K) is trivial.
        # Therefore, the conclusion is equivalent to: alg_closed == sep_closed.
        # The negation of the conclusion is: alg_closed != sep_closed.
        neg_q = (alg_closed != sep_closed)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "¬Q: K is algebraically closed XOR Gal(K^{sep}/K) is trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1