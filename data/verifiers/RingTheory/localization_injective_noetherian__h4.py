import sympy
from sympy import symbols

# Top-level setup
# (Abstract ring theory properties are not natively evaluable in SymPy, 
# so we expect a mock witness object or dictionary containing the truth values.)
Z = sympy.ZZ
Q = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy does not implement module theory or injective/Noetherian checks,
    this verifier expects the witness to be a dictionary or an object with attributes
    representing the truth values of the conditions.
    """
    def get_bool(names, default=False):
        if isinstance(witness, dict):
            for name in names:
                if name in witness:
                    return bool(witness[name])
        else:
            for name in names:
                if hasattr(witness, name):
                    return bool(getattr(witness, name))
        return default

    try:
        h1 = get_bool([
            'R is a commutative ring with identity',
            'is_commutative_ring_with_identity',
            'is_commutative_ring',
            'is_commutative',
            'commutative'
        ])
    except Exception:
        h1 = False

    try:
        h2 = get_bool([
            'R is a Noetherian ring',
            'is_noetherian_ring',
            'is_noetherian',
            'noetherian'
        ])
    except Exception:
        h2 = False

    try:
        h3 = get_bool([
            'E is an injective R-module',
            'is_injective_R_module',
            'is_injective_module',
            'E_is_injective',
            'injective'
        ])
    except Exception:
        h3 = False

    try:
        q = get_bool([
            'The localized module S^{-1}E is an injective S^{-1}R-module',
            'is_injective_S_inv_R_module',
            'localized_is_injective',
            'S_inv_E_is_injective',
            'conclusion'
        ], default=True)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: E is an injective R-module",
    "¬Q: The localized module S^{-1}E is not an injective S^{-1}R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3