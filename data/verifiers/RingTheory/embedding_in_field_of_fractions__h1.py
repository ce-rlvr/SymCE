import sympy
from sympy import S

# Top-level setup for standard ring/field objects
Z = S.Integers
Q = S.Rationals

def check_attr(obj, attrs, default=False):
    """Helper to safely check a list of boolean attributes/methods on an object."""
    for attr in attrs:
        if hasattr(obj, attr):
            try:
                val = getattr(obj, attr)
                if callable(val):
                    val = val()
                if val is not None:
                    return bool(val)
            except Exception:
                continue
    return default

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "Every integral domain can be embedded in a field."
    (The true theorem requires the domain to be commutative).
    """
    # Fallback for string-based witnesses
    if isinstance(witness, str):
        w = witness.lower()
        # A non-commutative domain cannot be embedded in a field.
        is_noncomm_domain = any(x in w for x in [
            'quaternion', 'malcev', 'weyl', 'free algebra', 
            'skew field', 'division ring', 'non-commutative domain'
        ])
        if is_noncomm_domain:
            return [True, True]
        return [False, False]

    # H_1: R is an integral domain (i.e., a ring with no zero divisors)
    try:
        h1 = check_attr(witness, [
            'is_integral_domain',
            'is_IntegralDomain',
            'is_domain',
            'is_Domain',
            'has_no_zero_divisors',
            'is_division_ring',
            'is_skew_field'
        ], default=False)
    except Exception:
        h1 = False

    # ¬Q: R cannot be embedded in a field
    # A domain can be embedded in a field iff it is commutative.
    try:
        if hasattr(witness, 'can_embed_in_field'):
            val = getattr(witness, 'can_embed_in_field')
            can_embed = bool(val() if callable(val) else val)
            neg_q = not can_embed
        else:
            # If it is a domain, it embeds in a field iff it is commutative.
            # Thus, it fails to embed iff it is NOT commutative.
            is_comm = check_attr(witness, [
                'is_commutative',
                'is_commutative_ring'
            ], default=True)
            neg_q = not is_comm
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R cannot be embedded in a field"
]

N_HYP = 1
NEG_Q_INDEX = 1