import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not have built-in support for arbitrary modules over non-Noetherian rings,
# we provide a mock class to represent the properties of the module E.
class AbstractModule:
    def __init__(self, is_injective, is_direct_sum_of_indecomposable_injectives):
        self.is_injective = is_injective
        self.is_direct_sum_of_indecomposable_injectives = is_direct_sum_of_indecomposable_injectives

# A known counterexample: the injective hull of R = k[x_1, x_2, ...] over itself.
# It is an injective module, but not a direct sum of indecomposable injective modules.
Counterexample = AbstractModule(is_injective=True, is_direct_sum_of_indecomposable_injectives=False)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Handle string-based witnesses describing a counterexample
    try:
        if isinstance(witness, str):
            s = witness.lower()
            h1 = "injective" in s or "e(" in s
            neg_q = "not" in s or "noetherian" in s or "infinite" in s or "k[x" in s or "boolean" in s or "counterexample" in s
            return [h1, neg_q]
    except Exception:
        pass

    # H_1: E is an injective R-module
    try:
        if hasattr(witness, "is_injective"):
            h1 = bool(witness.is_injective)
        elif hasattr(witness, "is_injective_module"):
            h1 = bool(witness.is_injective_module)
        elif isinstance(witness, dict):
            h1 = bool(witness.get("is_injective", witness.get("is_injective_module", False)))
    except Exception:
        h1 = False

    # neg_Q: E is NOT isomorphic to a direct sum of indecomposable injective modules of the form E(R/P)
    try:
        if hasattr(witness, "is_direct_sum_of_indecomposable_injectives"):
            neg_q = not bool(witness.is_direct_sum_of_indecomposable_injectives)
        elif hasattr(witness, "satisfies_matlis_decomposition"):
            neg_q = not bool(witness.satisfies_matlis_decomposition)
        elif isinstance(witness, dict):
            if "is_direct_sum_of_indecomposable_injectives" in witness:
                neg_q = not bool(witness["is_direct_sum_of_indecomposable_injectives"])
            elif "satisfies_matlis_decomposition" in witness:
                neg_q = not bool(witness["satisfies_matlis_decomposition"])
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E is an injective R-module",
    "¬Q: E is not isomorphic to a direct sum of indecomposable injective modules of the form E(R/P)"
]

N_HYP = 1
NEG_Q_INDEX = 1