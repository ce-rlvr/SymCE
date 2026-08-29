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
x, y, z, t = sympy.symbols('x y z t')

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a SymPy domain (e.g., GF(2).frac_field(x)) 
    or a tuple (domain, p).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, p_wit = witness
        else:
            F = witness
            p_wit = getattr(F, 'characteristic', 0)
            
        is_field = getattr(F, 'is_Field', False)
        char_F = getattr(F, 'characteristic', -1)
        
        # H_1: The characteristic of F is p
        # This implies F is a field, and its characteristic is a prime p > 0
        h1 = bool(is_field and char_F == p_wit and char_F > 0 and sympy.isprime(char_F))
    except Exception:
        h1 = False

    try:
        neg_q = False
        if h1:
            # Conclusion Q: The map phi(x) = x^p is a field automorphism of F
            # neg_Q: phi is NOT an automorphism (i.e., F is imperfect, phi is not surjective)
            if getattr(F, 'is_FiniteField', False):
                neg_q = False
            elif type(F).__name__ == 'FractionField':
                neg_q = True
            elif hasattr(F, 'gens') and len(F.gens) > 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of F is p",
    "¬Q: The map phi(x) = x^p is not a field automorphism of F"
]

N_HYP = 1
NEG_Q_INDEX = 1