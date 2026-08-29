import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# The conjecture involves abstract rings where counterexamples are typically
# infinite rings without identity. We provide standard symbols for convenience.

def _check_prop(witness, prop_names):
    """
    Helper to extract boolean properties from a custom witness object, dictionary,
    or a tuple containing the witness components.
    """
    if isinstance(prop_names, str):
        prop_names = [prop_names]
        
    items_to_check = [witness]
    if isinstance(witness, (list, tuple)):
        items_to_check.extend(witness)
        
    for prop in prop_names:
        for item in items_to_check:
            if isinstance(item, dict) and prop in item:
                val = item[prop]
                return bool(val()) if callable(val) else bool(val)
            if hasattr(item, prop):
                val = getattr(item, prop)
                return bool(val()) if callable(val) else bool(val)
                
    raise ValueError(f"Properties {prop_names} not found on witness")

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since no finite or finite-dimensional counterexamples exist for this theorem 
    (the dropped hypothesis is that R has an identity), the witness is expected 
    to be a custom object or dictionary representing the infinite counterexample 
    and exposing the necessary boolean flags/methods.
    """
    try:
        # H_1: I is a proper ideal of R
        h1 = _check_prop(witness, ['is_proper_ideal', 'proper_ideal'])
    except Exception:
        h1 = False

    try:
        # H_2: The quotient ring R/I is a free R-module
        h2 = _check_prop(witness, ['is_free_module', 'free_module', 'is_free_R_module'])
    except Exception:
        h2 = False

    try:
        # Conclusion Q: I = {0}
        # We want neg_Q to be True when the conclusion FAILS (i.e., I is NOT the zero ideal)
        q = _check_prop(witness, ['is_zero_ideal', 'zero_ideal'])
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: The quotient ring R/I is a free R-module",
    "¬Q: I is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2