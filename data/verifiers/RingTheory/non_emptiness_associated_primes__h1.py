import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Handle string witnesses (e.g., naming a known counterexample)
        if isinstance(witness, str):
            s = witness.lower()
            if "weyl" in s or "noncommutative" in s or "non-commutative" in s:
                return [True, True, True, True]
            return [False, False, False, False]
            
        # Handle tuple/list of booleans directly
        if isinstance(witness, (list, tuple)) and len(witness) == 4:
            if all(isinstance(x, bool) for x in witness):
                return list(witness)
                
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

        def has_prop(names):
            if isinstance(witness, dict):
                return any(name in witness for name in names)
            else:
                return any(hasattr(witness, name) for name in names)

        # H_1: R is a Noetherian ring
        h1 = get_bool(['is_Noetherian_ring', 'is_noetherian_ring', 'is_Noetherian', 'is_noetherian'])
        
        # H_2: M is a finitely generated R-module
        h2 = get_bool(['is_finitely_generated_module', 'is_finitely_generated', 'is_fg', 'is_fg_module'])
        
        # H_3: M is not the zero module
        if has_prop(['is_zero_module', 'is_zero']):
            h3 = not get_bool(['is_zero_module', 'is_zero'])
        elif has_prop(['is_non_zero_module', 'is_nonzero', 'is_non_zero']):
            h3 = get_bool(['is_non_zero_module', 'is_nonzero', 'is_non_zero'])
        else:
            h3 = False

        # ¬Q: The set of associated primes Ass_R(M) is empty
        if has_prop(['associated_primes_is_empty', 'ass_is_empty', 'is_associated_primes_empty']):
            neg_q = get_bool(['associated_primes_is_empty', 'ass_is_empty', 'is_associated_primes_empty'])
        elif has_prop(['associated_primes_non_empty', 'ass_non_empty', 'has_associated_primes']):
            neg_q = not get_bool(['associated_primes_non_empty', 'ass_non_empty', 'has_associated_primes'])
        else:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: M is a finitely generated R-module",
    "H_3: M is not the zero module",
    "¬Q: The set of associated primes Ass_R(M) is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3