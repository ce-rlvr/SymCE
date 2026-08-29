import sympy
import sympy.polys
import math
import itertools
import functools

# Top-level setup
class AlgebraicIntegersRing:
    """
    The ring of all algebraic integers.
    It is an integral domain.
    It has no irreducible elements (since for any non-unit x, x = sqrt(x) * sqrt(x), and sqrt(x) is not a unit).
    Vacuously, every irreducible element is prime.
    It is not a UFD because elements cannot be factored into irreducibles.
    """
    is_integral_domain = True
    irreducibles_are_prime = True
    is_UFD = False

# Provide a named binding for the witness expression to reference
Z_bar = AlgebraicIntegersRing()

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: Every irreducible element in R is a prime element",
    "¬Q: R is not a unique factorization domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_prop(witness, prop_names):
    """Helper to safely extract boolean properties from dicts or objects."""
    if isinstance(witness, dict):
        for p in prop_names:
            if p in witness:
                return bool(witness[p])
    else:
        for p in prop_names:
            if hasattr(witness, p):
                val = getattr(witness, p)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                return bool(val)
    return None

def is_sympy_domain(witness):
    """Check if the witness is a SymPy Domain without strict imports."""
    try:
        for cls in type(witness).__mro__:
            if cls.__name__ == 'Domain' and 'sympy.polys' in cls.__module__:
                return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    try:
        h1_val = get_prop(witness, ['is_integral_domain', 'is_IntegralDomain', 'is_domain'])
        if h1_val is not None:
            h1 = h1_val
        else:
            # Fallback: SymPy domains are generally integral domains
            h1 = is_sympy_domain(witness)
    except Exception:
        h1 = False

    # H_2: Every irreducible element in R is a prime element
    try:
        h2_val = get_prop(witness, ['irreducibles_are_prime', 'every_irreducible_is_prime', 'has_no_irreducibles'])
        if h2_val is not None:
            h2 = h2_val
        else:
            # Fallback: In a UFD, all irreducibles are prime.
            ufd_val = get_prop(witness, ['is_UFD', 'is_ufd'])
            h2 = bool(ufd_val)
    except Exception:
        h2 = False

    # ¬Q: R is not a unique factorization domain
    try:
        neg_q_val = get_prop(witness, ['is_UFD', 'is_ufd'])
        if neg_q_val is not None:
            neg_q = not neg_q_val
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]