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

# Top-level setup for potential witness expressions
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a dictionary of properties, a tuple (R, x), or an object R with attribute x.
    """
    if isinstance(witness, dict):
        if 'R' in witness and 'x' in witness:
            R = witness['R']
            x = witness['x']
        else:
            try:
                h1 = bool(witness.get('is_integral_domain', False))
                h2 = not bool(witness.get('is_zero', True)) and not bool(witness.get('is_unit', True))
                factors = True
                for k in ['is_finite_product_of_irreducibles', 'factors_into_irreducibles', 'has_irreducible_factorization']:
                    if k in witness:
                        factors = witness[k]
                        break
                neg_q = not bool(factors)
                return [h1, h2, neg_q]
            except Exception:
                return [False, False, False]
    else:
        R = witness
        x = None
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        elif hasattr(witness, 'x'):
            x = witness.x

    # H_1: R is an integral domain
    h1 = False
    try:
        if hasattr(R, 'is_integral_domain'):
            val = R.is_integral_domain
            h1 = bool(val() if callable(val) else val)
        elif hasattr(R, 'is_domain'):
            val = R.is_domain
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # H_2: x is a non-zero, non-unit element of R
    h2 = False
    try:
        if x is not None:
            is_zero = False
            if hasattr(R, 'is_zero'):
                is_zero = R.is_zero(x)
            elif hasattr(x, 'is_zero'):
                val = x.is_zero
                is_zero = val() if callable(val) else val
            elif hasattr(R, 'zero'):
                is_zero = (x == R.zero)
            else:
                is_zero = (x == 0)
                
            is_unit = False
            if hasattr(R, 'is_unit'):
                is_unit = R.is_unit(x)
            elif hasattr(x, 'is_unit'):
                val = x.is_unit
                is_unit = val() if callable(val) else val
                
            h2 = bool((not is_zero) and (not is_unit))
    except Exception:
        pass

    # ¬Q: x cannot be expressed as a finite product of irreducible elements of R
    neg_q = False
    try:
        found = False
        for attr in ['is_finite_product_of_irreducibles', 'factors_into_irreducibles', 'has_irreducible_factorization']:
            if hasattr(R, attr):
                val = getattr(R, attr)
                if callable(val):
                    try:
                        res = val(x)
                    except TypeError:
                        res = val()
                else:
                    res = val
                neg_q = not bool(res)
                found = True
                break
            elif hasattr(x, attr):
                val = getattr(x, attr)
                res = val() if callable(val) else val
                neg_q = not bool(res)
                found = True
                break
        if not found:
            neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: x is a non-zero, non-unit element of R",
    "¬Q: x cannot be expressed as a finite product of irreducible elements of R"
]

N_HYP = 2
NEG_Q_INDEX = 2