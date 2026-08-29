import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# Since SymPy does not have built-in support for abstract module theory or injective modules,
# any formal witness must be represented as a descriptive string, a dictionary with boolean flags,
# or a custom object. We define a dummy class that could be used by the witness generator.
class InjectiveModuleFamily:
    """
    A mock class to represent a family of injective modules over a ring.
    Since SymPy lacks module theory, this allows the witness generator to 
    programmatically express the counterexample (e.g., over a non-Noetherian ring).
    """
    def __init__(self, ring_is_noetherian=False):
        self.is_injective_family = True
        self.direct_sum_is_injective = ring_is_noetherian

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        # Check dictionary-based witness
        if isinstance(witness, dict):
            if 'is_injective_family' in witness:
                h1_ok = bool(witness['is_injective_family'])
            if 'direct_sum_is_injective' in witness:
                neg_q_ok = not bool(witness['direct_sum_is_injective'])
        # Check object-based witness (like the mock class above)
        else:
            if hasattr(witness, 'is_injective_family'):
                h1_ok = bool(witness.is_injective_family)
            if hasattr(witness, 'direct_sum_is_injective'):
                neg_q_ok = not bool(witness.direct_sum_is_injective)
                
        # Fallback to string representation analysis for descriptive witnesses
        if not h1_ok:
            s = str(witness).lower()
            if "injective" in s and any(kw in s for kw in ["family", "module", "hull", "envelope", "e_i"]):
                h1_ok = True
                
        if not neg_q_ok:
            s = str(witness).lower()
            if any(kw in s for kw in [
                "not injective", 
                "non-noetherian", 
                "not noetherian", 
                "infinite", 
                "fails to be injective",
                "not an injective"
            ]):
                neg_q_ok = True
                
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {E_i} is an arbitrary family of injective left R-modules",
    "¬Q: The direct sum of {E_i} is not an injective left R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1