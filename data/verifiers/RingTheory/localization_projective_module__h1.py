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
Z = sympy.S.Integers
Q = sympy.S.Rationals

def evaluate_prop(witness, prop_names, default):
    for prop in prop_names:
        try:
            if isinstance(witness, dict) and prop in witness:
                return bool(witness[prop])
            if hasattr(witness, prop):
                val = getattr(witness, prop)
                if callable(val):
                    return bool(val())
                return bool(val)
        except Exception:
            pass
    return default

def conditions(witness) -> list[bool]:
    h1 = evaluate_prop(witness, [
        'P_is_projective_R_module', 
        'is_projective', 
        'P_is_projective',
        'is_projective_module'
    ], False)
    
    h2 = evaluate_prop(witness, [
        'S_is_multiplicatively_closed', 
        'is_multiplicatively_closed', 
        'S_is_multiplicatively_closed_subset'
    ], False)
    
    q = evaluate_prop(witness, [
        'localized_is_projective', 
        'S_inv_P_is_projective', 
        'is_localized_projective',
        'localized_module_is_projective'
    ], True)
    
    return [h1, h2, not q]

CONDITION_LABELS = [
    "H_1: P is a projective R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized module S^{-1}P is not a projective S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2